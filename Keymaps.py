# -*- coding: utf-8 -*-
import os
import threading
import logging
import sublime, sublime_plugin
import functools
import codecs, json, re, string
from itertools import groupby
from datetime import datetime
from collections import namedtuple

MY_NAME = 'Keymaps'

DEBUG = True

GLOBAL_SETTINGS = sublime.load_settings("Preferences.sublime-settings")

DEFAULT_SETTINGS = {
	'keymaps_title': MY_NAME + ' Cheat Sheet',
	'show_osx_keys': False	# Let's give some love to Winux guys ;)
}

platforms = {'linux': 'Linux', 'osx': 'OSX', 'windows': 'Windows'}

FILE_NAME = 1

#shameless copy paste from json/decoder.py
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'[ \t\n\r]*', FLAGS)

## LOGGING SETUP
try:
	from logging import NullHandler
except ImportError:
	class NullHandler(logging.Handler):
	
		def handle(self, record):
			pass
	
		def emit(self, record):
			pass
	
		def createLock(self):
			self.lock = None

log = logging.getLogger(MY_NAME)
log.handlers = [] ## hack to prevent extraneous handlers on ST2 auto-reload
log.addHandler(NullHandler())
log.setLevel(logging.INFO)
if DEBUG:
	log.addHandler(logging.StreamHandler())
	log.setLevel(logging.DEBUG)


def find_keymap(view, data):
	new_view = view.window().open_file(os.path.join(sublime.packages_path(), data['package'], 'Default (' + platforms[sublime.platform()] + ').sublime-keymap'))
	do_when(lambda: not new_view.is_loading(), lambda: find_km(new_view, data['keys'][len(data['keys'])-1]))


def find_km(new_view, keymap):
	new_view.window().run_command("show_panel", {"panel": "find"})
	new_view.window().run_command("insert", {"characters": keymap})


def do_when(conditional, callback, *args, **kwargs):
	if conditional():
		return callback(*args, **kwargs)
	sublime.set_timeout(functools.partial(do_when, conditional, callback, *args, **kwargs), 50)


class Settings(dict):
	"""Combine default and user settings"""
	def __init__(self, user_settings):
		settings = DEFAULT_SETTINGS.copy()
		settings.update(user_settings)
		super(Settings, self).__init__(settings)


class KeymapsCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		window = self.view.window()
		settings = Settings(self.view.settings().get('keymaps', {}))

		keymap_counter = KeymapScanCounter()
		extractor = KeymapsExtractor(settings, keymap_counter)
		renderer = KeymapsRenderer(settings, window, keymap_counter)
		worker_thread = WorkerThread(extractor, renderer)
		worker_thread.start()
		ThreadProgress(worker_thread, 'Finding ' + MY_NAME, 'Done.', keymap_counter)


class KeymapsExtractor(object):

	def __init__(self, settings, keymap_counter):
		self.ignored = GLOBAL_SETTINGS.get("ignored_packages", [])
		self.settings = settings
		self.keymap_counter = keymap_counter
		self.log = logging.getLogger(MY_NAME + '.extractor')


	def removeComments(self, string):
		# remove all occurance streamed comments (/* COMMENT */) from string
		string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,string)
		# remove all occurance singleline comments (// COMMENT\n ) from string
		string = re.sub(re.compile("//.*?\n" ) ,"" ,string)
		return string


	def parseJSON(self, path):
		parsedJSON = ''
		if not os.path.isfile(path):
			return parsedJSON
		with codecs.open(path) as f:
			content = self.removeComments(f.read())
		if f is not None:
			f.close()
		try:
			parsedJSON = json.loads(content, cls=ConcatJSONDecoder)
		except (ValueError):
			return ''
		return parsedJSON[0]


	def getCaption(self, commands, keys):
		for dict in commands:
			if dict['command'] != keys['command']:
				continue
			if not 'subcommand' in keys:
				return dict['caption']
			if not 'args' in dict:
				continue
			args = dict['args']
			if not 'command' in args:
				continue
			if not args['command'] == keys['subcommand']:
				continue
			return dict['caption']
		return ''


	def getCaptions(self, packages):
		ppath = sublime.packages_path()
		cxt = 'Default.sublime-commands'
		for package in packages:
			if not 'keymaps' in package:
				continue
			for keymap in package['keymaps']:
				if not 'keys' in keymap:
					continue
				commands = self.parseJSON(os.path.join(ppath, package['package'], cxt))
				if not isinstance(commands, list):
					continue

				caption = self.getCaption(commands, keymap)
				if caption == '':
					continue
				keymap['caption'] = caption


	def getKeymaps(self):
		self.packages = []
		kxt = ['Default (' + platforms[sublime.platform()] + ').sublime-keymap']
		for root, dirs, files in os.walk(sublime.packages_path()):
			self.package = {}
			for file in files:
				if not file in kxt:
					continue
				package = os.path.split(root)[FILE_NAME]
				if package in self.ignored:
					continue
				keymaps = self.parseJSON(os.path.join(root, file))
				if not isinstance(keymaps, list):
					continue

				kmaps = []
				for keymap in keymaps:
					item = {}
					keys = keymap.get('keys')
					if not keys:
						continue
					command = keymap.get('command')
					if not command:
						continue
					item = {
						'keys': keys,
						'command': command
					}
					args = keymap.get('args')
					if args:
						if 'command' in args:
							item['subcommand'] = args['command']
					kmaps.append(item)
				self.package = { 'package': package, 'keymaps': kmaps }
			if not self.package:
				continue
			self.packages.append(self.package)
			self.keymap_counter.increment()
		return self.packages


	def extract(self):
		self.keymap_counter.reset()
		keyMaps = self.getKeymaps()
		if keyMaps:
			self.getCaptions(keyMaps)
			kxt = ['Default (' + platforms[sublime.platform()] + ').sublime-keymap']
			for keyMap in keyMaps:
				for keys in keyMap['keymaps']:
					self.keymap_counter.increment()
					caption = keys['command']
					if 'caption' in keys:
						caption = keys['caption']
					yield {'package': keyMap['package'], 'keys': keys['keys'], 'caption': caption}


class KeymapsRenderer(object):

	def __init__(self, settings, window, keymap_counter):
		self.settings = settings
		self.window = window
		self.keymap_counter = keymap_counter

	@property
	def view_name(self):
		"""The name of the new keymaps view. Defined in settings."""
		return self.settings['keymaps_title']

	@property
	def header(self):
		hr = u'+ {0} +'.format('-' * 76)
		hr_ = u'{hr}\n| ' + MY_NAME + ' @ {0:<' + str(73 - MY_NAME.__len__()) + '} |\n| {1:<76} |\n{hr}\n'
		return hr_.format(datetime.now().strftime('%A %d %B %Y %H:%M').decode("utf-8"),
			u'{0} keymaps found'.format(self.keymap_counter),
			hr=hr)

	@property
	def view(self):
		existing_keymaps = [v for v in self.window.views() 
							if v.name() == self.view_name and v.is_scratch()]
		if existing_keymaps:
			v = existing_keymaps[0]
		else:
			v = self.window.new_file()
			v.set_name(self.view_name)
			v.set_scratch(True)
			v.settings().set('cheat_sheet', True)
		return v


	def format(self, packages):
		key_func = lambda m: m['package']
		packages = sorted(packages, key=key_func)
		myKeymaps = {}

		for message_type, matches in groupby(packages, key=key_func):
			matches = list(matches)
			if matches:
				yield ('header', u'\n {0} ({1})'.format(message_type.decode('utf8', 'ignore'), len(matches)), {})
				for idx, m in enumerate(matches, 1):
					keys = ' ], [ '.join(m['keys']).decode('utf8', 'ignore').upper().replace('+', ' ')
					if sublime.platform() == 'osx' and self.settings['show_osx_keys']:
						keys = keys.replace('CTRL', u'⌃').replace('ALT', u'⌥').replace('SUPER', u'⌘').replace('SHIFT', u'⇧')
					line = u"\t{keys}: {caption}".format(keys='[ '+keys+' ]', caption=m['caption'])
					yield ('keymap', line, m)


	def render_to_view(self, formatted_keymaps):
		"""This blocks the main thread, so make it quick"""
		## Header
		keymaps_view = self.view
		edit = keymaps_view.begin_edit()
		keymaps_view.erase(edit, sublime.Region(0, keymaps_view.size()))
		keymaps_view.insert(edit, keymaps_view.size(), self.header)
		keymaps_view.end_edit(edit)

		## Region : match_dicts
		regions = {}

		## Result sections
		for linetype, line, data in formatted_keymaps:
			edit = keymaps_view.begin_edit()
			insert_point = keymaps_view.size()
			keymaps_view.insert(edit, insert_point, line)
			if linetype == 'keymap':
				rgn = sublime.Region(insert_point, keymaps_view.size())
				regions[rgn] = data
			keymaps_view.insert(edit, keymaps_view.size(), u'\n')
			keymaps_view.end_edit(edit)


		keymaps_view.add_regions('keymaps', regions.keys(), '')

		## Store {Region : data} map in settings
		## TODO: Abstract this out to a storage class Storage.get(region) ==> data dict
		## Region() cannot be stored in settings, so convert to a primitive type
		# d_ = regions
		d_ = dict(('{0},{1}'.format(k.a, k.b), v) for k, v in regions.iteritems())
		keymaps_view.settings().set('keymap_regions', d_)

		## Set syntax and settings
		keymaps_view.set_syntax_file('Packages/' + MY_NAME + '/cheat_sheet.hidden-tmLanguage')
		keymaps_view.settings().set('line_padding_bottom', 2)
		keymaps_view.settings().set('line_padding_top', 2)
		keymaps_view.settings().set('word_wrap', False)
		keymaps_view.settings().set('command_mode', True)
		self.window.focus_view(keymaps_view)


class WorkerThread(threading.Thread):

	def __init__(self, extractor, renderer):
		self.extractor = extractor
		self.renderer = renderer
		threading.Thread.__init__(self)


	def run(self):
		## Extract in this thread
		keymaps = self.extractor.extract()
		rendered = list(self.renderer.format(keymaps))

		## Render into new window in main thread
		def render():
			self.renderer.render_to_view(rendered)

		sublime.set_timeout(render, 10)


class ThreadProgress(object):

	def __init__(self, thread, message, success_message, keymap_counter):
		self.thread = thread
		self.message = message
		self.success_message = success_message
		self.keymap_counter = keymap_counter
		self.addend = 1
		self.size = 8
		sublime.set_timeout(lambda: self.run(0), 100)


	def run(self, i):
		if not self.thread.is_alive():
			if hasattr(self.thread, 'keymap') and not self.thread.keymap:
				sublime.status_message('')
				return
			sublime.status_message(self.success_message)
			return

		before = i % self.size
		after = (self.size - 1) - before
		sublime.status_message('%s [%s=%s] (%s files scanned)' % \
			(self.message, ' ' * before, ' ' * after, self.keymap_counter))
		if not after:
			self.addend = -1
		if not before:
			self.addend = 1
		i += self.addend
		sublime.set_timeout(lambda: self.run(i), 100)


class NavigateKeymaps(sublime_plugin.TextCommand):
	DIRECTION = {'forward': 1, 'backward': -1}
	STARTING_POINT = {'forward': -1, 'backward': 0}

	def __init__(self, view):
		super(NavigateKeymaps, self).__init__(view)


	def run(self, edit, direction):
		view = self.view
		settings = view.settings()
		keymaps = self.view.get_regions('keymaps')
		if not keymaps:
			sublime.status_message('No keymaps to navigate')
			return

		##NOTE: numbers stored in settings are coerced to floats or longs
		selection = int(settings.get('selected_keymap', self.STARTING_POINT[direction]))
		selection = selection + self.DIRECTION[direction]
		try:
			target = keymaps[selection]
		except IndexError:
			target = keymaps[0]
			selection = 0

		settings.set('selected_keymap', selection)
		## Create a new region for highlighting
		target = target.cover(target)
		view.add_regions('selection', [target], 'selected', 'dot')
		view.show(target)


class ClearSelection(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.erase_regions('selection')
		self.view.settings().erase('selected_keymap')


class GotoKeymap(sublime_plugin.TextCommand):

	def __init__(self, *args):
		self.log = logging.getLogger(MY_NAME + '.nav')
		super(GotoKeymap, self).__init__(*args)


	def run(self, edit):
		## Get the idx of selected keymap region
		selection = int(self.view.settings().get('selected_keymap', -1))
		## Get the region
		selected_region = self.view.get_regions('keymaps')[selection]
		## Convert region to key used in keymaps_regions (this is tedious, but 
		##	there is no other way to store regions with associated data)
		data = self.view.settings().get('keymap_regions')['{0},{1}'.format(selected_region.a, selected_region.b)]
		self.log.debug(u'Goto keymap at {package}'.format(**data))
		## Open file for edit
		find_keymap(self.view, data)


class MouseGotoKeymap(sublime_plugin.TextCommand):

	def __init__(self, *args):
		self.log = logging.getLogger(MY_NAME + '.nav')
		super(MouseGotoKeymap, self).__init__(*args)


	def highlight(self, region):
		target = region.cover(region)
		self.view.add_regions('selection', [target], 'selected', 'dot')
		self.view.show(target)


	def get_keymaps_region(self, pos):
		line = self.view.line(pos)
		return line


	def run(self, edit):
		if not self.view.settings().get('keymap_regions'):
			return
		## get selected line
		pos = self.view.sel()[0].end()
		print pos
		keymap = self.get_keymaps_region(pos)
		self.highlight(keymap)
		data = self.view.settings().get('keymap_regions')['{0},{1}'.format(keymap.a, keymap.b)]
		self.log.debug(u'Goto keymap at {package}'.format(**data))
		## Open file for edit
		find_keymap(self.view, data)


class ConcatJSONDecoder(json.JSONDecoder):

	def decode(self, s, _w=WHITESPACE.match):
		s_len = len(s)

		objs = []
		end = 0
		while end != s_len:
			obj, end = self.raw_decode(s, idx=_w(s, end).end())
			end = _w(s, end).end()
			objs.append(obj)
		return objs


class KeymapScanCounter(object):
	"""Thread-safe counter used to update the status bar"""
	def __init__(self):
		self.ct = 0
		self.lock = threading.RLock()
		self.log = logging.getLogger(MY_NAME)


	def __call__(self, filepath):
		self.log.debug(u'Scanning %s' % filepath)
		self.increment()


	def __str__(self):
		with self.lock:
			return '%d' % self.ct


	def increment(self):
		with self.lock:
			self.ct += 1


	def reset(self):
		with self.lock:
			self.ct = 0
