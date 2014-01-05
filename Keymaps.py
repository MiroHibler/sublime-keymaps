# -*- coding: utf-8 -*-
import os
import threading
import logging
import sublime, sublime_plugin
import functools
import codecs, json, re, string
from itertools import groupby
from datetime import datetime

DEBUG = True

ST2 = sublime.version() < '3000'

LINE_SIZE = 80

MY_NAME = 'Keymaps'
VERSION = '1.3.1'

DEFAULT_SETTINGS = {
	'keymaps_title': MY_NAME + ' Cheat Sheet',
	'show_pretty_keys': False	# Let's give some love to Winux guys too ;)
}

PLATFORMS = {'linux': 'Linux', 'osx': 'OSX', 'windows': 'Windows'}

# To properly sort modifier keys
TOKENS = ['CTRL', 'ALT', 'OPTION', 'SHIFT', 'SUPER']
# To properly sort F-keys
FTOKENS = {
	'F1': 'F01',
	'F2': 'F02',
	'F3': 'F03',
	'F4': 'F04',
	'F5': 'F05',
	'F6': 'F06',
	'F7': 'F07',
	'F8': 'F08',
	'F9': 'F09'
}

PRETTY_KEYS = {
	'CTRL': u'\u2303',
	'ALT': u'\u2387',
	'OPTION': u'\u2387',
	'SUPER': u'\u2318',
	'SHIFT': u'\u21E7',
	'FORWARD_SLASH': u'/',
	'BACKWARD_SLASH': u'\\',
	'ENTER': u'\u23CE',
	'LEFT': u'\u2190',
	'UP': u'\u2191',
	'RIGHT': u'\u2192',
	'DOWN': u'\u2193',
	'TAB': u'\u21E5',
	'SPACE': u'\u2423',
	'INSERT': u'\u2380',
	'BACKSPACE': u'\u232B',
	'DELETE': u'\u2326',
	'CLEAR': u'\u2327',
	'ESCAPE': u'\u238B',
	'HOME': u'\u2353',
	'END': u'\u234C',
	'PAGEUP': u'\u235E',
	'PAGEDOWN': u'\u2357',
	'BREAK': u'\u2386',
	'BACKQUOTE': u'\u0060',
	'PLUS': u'+',
	'EQUALS': u'=',
	'MINUS': u'-',
	'F01': u'F1',
	'F02': u'F2',
	'F03': u'F3',
	'F04': u'F4',
	'F05': u'F5',
	'F06': u'F6',
	'F07': u'F7',
	'F08': u'F8',
	'F09': u'F9'
}

if sublime.platform() == 'osx':
	PRETTY_KEYS['ALT'] = u'\u2325'
	PRETTY_KEYS['OPTION'] = u'\u2325'

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

"""
	Main stuff
"""
def find_keymap(view, data):
	path = os.path.join(sublime.packages_path(), data['package'], 'Default (' + PLATFORMS[sublime.platform()] + ').sublime-keymap')
	if not os.path.isfile(path):
		em = MY_NAME + ':\n\nIt seems that this keymap is defined either in global keymap file\n\n'
		em = em + '(\'/Packages/Default/Default (' + PLATFORMS[sublime.platform()] + ').sublime-keymap\')\n\n'
		em = em + 'or in package\'s default keymap file\n\n'
		em = em + '(/Packages/' + data['package'] + '/Default (' + PLATFORMS[sublime.platform()] + ').sublime-keymap\')!\n\n'
		em = em + 'Would you like to open User\'s keymap file\n\n'
		em = em + '(/Packages/User/Default (' + PLATFORMS[sublime.platform()] + ').sublime-keymap\')\n\n'
		em = em + 'to create/edit this keymap?'
		answer = sublime.ok_cancel_dialog(em, 'Yes, let\'s do that...')
		if answer:
			path = os.path.join(sublime.packages_path(), 'User', 'Default (' + PLATFORMS[sublime.platform()] + ').sublime-keymap')
			new_view = view.window().open_file(path)
	else:
		new_view = view.window().open_file(path)
		do_when(lambda: not new_view.is_loading(), lambda: find_km(new_view, data['keys'][len(data['keys'])-1]))


def find_km(view, keys):
	view.window().run_command("show_panel", {"panel": "find"})
	view.window().run_command("insert", {"characters": '"' + '+'.join(keys).lower() + '"'})


def do_when(conditional, callback, *args, **kwargs):
	if conditional():
		return callback(*args, **kwargs)
	sublime.set_timeout(functools.partial(do_when, conditional, callback, *args, **kwargs), 50)


def do(renderer, keymap_counter):
	default_packages = ['Default']
	user_packages = ['User']
	global_settings = sublime.load_settings("Preferences.sublime-settings")
	ignored_packages = global_settings.get("ignored_packages", [])
	package_control_settings = sublime.load_settings("Package Control.sublime-settings")
	installed_packages = package_control_settings.get("installed_packages", [])
	if len(installed_packages) == 0:
		includes = ('.sublime-package')
		os_packages = []
		for (root, dirs, files) in os.walk(sublime.installed_packages_path()):
			for file in files:
				if file.endswith(includes):
					os_packages.append(file.replace(includes, ''))
		for (root, dirs, files) in os.walk(sublime.packages_path()):
			for dir in dirs:
				os_packages.append(dir)
			break	# just the top level
		installed_packages = []
		[installed_packages.append(package) for package in os_packages if package not in installed_packages]

	diff = lambda l1,l2: [x for x in l1 if x not in l2]
	active_packages = diff( default_packages + installed_packages + user_packages, ignored_packages)

	keymapsExtractor = KeymapsExtractor(active_packages, keymap_counter)
	worker_thread = WorkerThread(keymapsExtractor, renderer)
	worker_thread.start()
	ThreadProgress(worker_thread, 'Searching ' + MY_NAME, 'Done.', keymap_counter)


class Settings(dict):
	"""Combine default and user settings"""
	def __init__(self, user_settings):
		settings = DEFAULT_SETTINGS.copy()
		settings.update(user_settings)
		super(Settings, self).__init__(settings)


class ConcatJSONDecoder(json.JSONDecoder):

	def decode(self, s, _w=WHITESPACE.match):
		s_len = len(s)
		bs = s

		objs = []
		end = 0
		while end != s_len:
			obj, end = self.raw_decode(bs, idx=_w(bs, end).end())
			end = _w(bs, end).end()
			objs.append(obj)
		return objs


class CheatSheetCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		settings = Settings(self.view.settings().get('keymaps', {}))
		keymap_counter = KeymapScanCounter()
		renderer = CheatSheetRenderer(settings, self.view.window(), keymap_counter)
		do(renderer, keymap_counter)


class FindKeymapCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		settings = Settings(self.view.settings().get('keymaps', {}))
		keymap_counter = KeymapScanCounter()
		renderer = FindKeymapRenderer(settings, self.view.window(), keymap_counter)
		do(renderer, keymap_counter)


class KeymapsExtractor(object):

	def __init__(self, active_packages, keymap_counter):
		self.active_packages = active_packages
		self.keymap_counter = keymap_counter
		self.log = logging.getLogger(MY_NAME + '.extractor')


	def removeComments(self, string):
		# remove all occurance streamed comments (/* COMMENT */) from string
		string = re.sub(re.compile(b"//.*?\n"), "", string)
		# remove all occurance singleline comments (// COMMENT\n ) from string
		string = re.sub(re.compile(b"/\*.*?\*/", re.DOTALL), "", string)
		return string


	def parseJSON(self, package, name, ext):
		if ST2:
			path = os.path.join(sublime.packages_path(), package, name + '.' + ext)
			if not os.path.isfile(path):
				path = os.path.join(sublime.packages_path(), package, 'Default.' + ext)
				if not os.path.isfile(path):
					return None
			with codecs.open(path) as f:
				content = self.removeComments(f.read())
			if f is not None:
				f.close()
			try:
				parsedJSON = json.loads(content, cls=ConcatJSONDecoder)
			except (ValueError):
				return None
			return parsedJSON[0]
		else:
			try:
				resource = sublime.load_resource('Packages/' + package + '/' + name + '.' + ext)
			except (IOError):
				try:
					resource = sublime.load_resource('Packages/' + package + '/Default.' + ext)
				except (IOError):
					return None
			return sublime.decode_value(resource)


	def getCaption(self, commands, keys):
		if commands:
			for dict in commands:
				if 'command' in dict:
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
				else:
					if 'caption' in dict:
						return dict['caption']
				return ''
		return ''


	def getCaptions(self, packages):
		for package in packages:
			commands = self.parseJSON(package['package'], 'Default', 'sublime-commands')
			for keymap in package['keymaps']:
				if not 'keys' in keymap:
					continue
				caption = self.getCaption(commands, keymap)
				if caption == '':
					caption = keymap['command'].replace('_', ' ').title()
				keymap['caption'] = caption


	def getKeymaps(self):
		packages = []
		for package in self.active_packages:
			keymaps = self.parseJSON(package, 'Default (' + PLATFORMS[sublime.platform()] + ')', 'sublime-keymap')

			if keymaps is not None:
				for keymap in keymaps:
					item = {'package': package}
					keys = keymap.get('keys')
					if not keys:
						continue
					item['keys'] = []
					for key_map in keys:
						km = key_map.replace(u' ', u'').upper().split('+')
						item['keys'].append(km)
					# Sort keys
					skeys = []
					for key_token in item['keys']:
						ktoks = []
						for token in TOKENS:
							if token in key_token:
								ktoks.append(u'' + token)
								key_token.remove(token)
						if not key_token[0]:
							continue
						if key_token[0] in FTOKENS:
							ktoks.append(FTOKENS[key_token[0]])
						else:
							ktoks.append(key_token[0])
						skeys.append(ktoks)
					item['keys'] = skeys
					# Get Command
					command = keymap.get('command')
					if not command:
						continue
					item['command'] = command
					# Get Args
					args = keymap.get('args')
					if args:
						if 'command' in args:
							item['subcommand'] = args['command']
						item['args'] = args
					# Get Context
					context = keymap.get('context')
					if context:
						item['context'] = []
						for ctxt in context:
							if 'key' in ctxt:
								item['context'].append(ctxt['key'])
					packages.append(item)

		# Merge keymaps in Order of Precedence (the way Sublime Text is doing it):
		# 1. Load	Default keymaps (Packages/Default/*.sublime-keymap)
		# 2. Merge	Packages keymaps (Packages/*/*.sublime-keymap)
		# 3. Merge	User keymaps (Packages/User/*.sublime-keymap)
		merged = []
		key_func = lambda m: m['keys']
		packages = sorted(packages, key=key_func)
		for keymap, matches in groupby(packages, key=key_func):
			matches = list(matches)
			if matches:
				if len(matches) > 1:
					key_f = lambda m: m['command']
					doubles = sorted(matches, key=key_f)
					for command, clones in groupby(doubles, key=key_f):
						clones = list(clones)
						if len(clones) > 1:
							unique = next((clone for clone in clones if clone['package'] == 'User'), None)
							if not unique:
								unique = next((clone for clone in clones if clone['package'] != 'Default'), None)
								if not unique:
									for unique in clones:
										merged.append(unique)
							else:
								merged.append(unique)
						else:
							merged.append(clones[0])
				else:
					merged.append(matches[0])

		packages = []
		key_func = lambda m: m['package']
		grouped = sorted(merged, key=key_func)
		for pack, matches in groupby(grouped, key=key_func):
			keymaps = list(matches)
			if keymaps:
				kmaps = []
				for keymap in keymaps:
					kmaps.append(keymap)
			packages.append({ 'package': pack, 'keymaps': kmaps })

		return packages


	def extract(self):
		self.keymap_counter.reset()
		keyMaps = self.getKeymaps()
		if keyMaps:
			self.getCaptions(keyMaps)
			for keyMap in keyMaps:
				for keys in keyMap['keymaps']:
					args = keys.get('args')
					if not args:
						args = None
					self.keymap_counter.increment()
					yield {'package': keyMap['package'], 'keys': keys['keys'], 'command': keys['command'], 'args': args, 'caption': keys['caption']}


class CheatSheetRenderer(object):

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
		hr = u'+ {0} +'.format('-' * (LINE_SIZE - 4))
		hr_ = u'{hr}\n| ' + MY_NAME + ' v' + VERSION + ' @ {0:<' + str(LINE_SIZE - 9 - MY_NAME.__len__() - VERSION.__len__()) + '} |\n| {1:<76} |\n{hr}\n'

		if self.settings['show_pretty_keys']:
			if sublime.platform() != 'osx':
				hr_ = hr_ + '\n' + u'{0} - CTRL, {1} - ALT, {2} - SHIFT'.format(PRETTY_KEYS['CTRL'], PRETTY_KEYS['ALT'], PRETTY_KEYS['SHIFT']).center(LINE_SIZE) + u'\n'

		return hr_.format(datetime.now().strftime('%A %d %B %Y %H:%M').encode('utf-8').decode('utf-8'),
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

		for package, keymaps in groupby(packages, key=key_func):
			keymaps = list(keymaps)
			if keymaps:
				yield ('header', u'{0} ({1})'.format(package, len(keymaps)), {})

				for idx, m in enumerate(keymaps, 1):
					keys = ''
					for key_token in m['keys']:
						keys = keys + u'[ ' + ' '.join(key_token) + u' ]'
					if self.settings['show_pretty_keys']:
						d = PRETTY_KEYS
						pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in d.keys()) + r')\b')
						keys = pattern.sub(lambda x: d[x.group()], keys)
					line = u'{0}: {1}'.format(keys.rjust(LINE_SIZE // 2), m['caption'])
					yield ('keymap', line, m)


	def render(self, formatted_keymaps):
		"""This blocks the main thread, so make it quick"""
		## Header
		keymaps_view = self.view
		## run_command('append') doesn't work well in ST2(?)
		if ST2:
			edit = keymaps_view.begin_edit()
			keymaps_view.erase(edit, sublime.Region(0, keymaps_view.size()))
			keymaps_view.insert(edit, keymaps_view.size(), self.header)
			keymaps_view.end_edit(edit)
		else: # ST3
			keymaps_view.run_command("select_all")
			keymaps_view.run_command("right_delete")
			keymaps_view.run_command('append', {'characters':self.header})

		## Region : match_dicts
		regions = {}

		## Keymap sections
		for linetype, line, data in formatted_keymaps:
			insert_point = keymaps_view.size()
			if ST2:
				edit = keymaps_view.begin_edit()
				if linetype == 'keymap':
					insert_space = insert_point
					line_ = line.lstrip()
					keymaps_view.insert(edit, insert_space, u'{0}'.format(' ' * (len(line)-len(line_))))
					insert_point = insert_space + (keymaps_view.size() - insert_space)
					keymaps_view.insert(edit, insert_point, line_)
					rgn = sublime.Region(insert_point, keymaps_view.size())
					regions[(rgn.a, rgn.b)] = (rgn, data)
				else: # 'header'
					# TODO: Check if this .rstrip() is doing right
					keymaps_view.insert(edit, insert_point, u'\n\n' + line.center(LINE_SIZE).rstrip() + u'\n')
				keymaps_view.insert(edit, keymaps_view.size(), u'\n')
				keymaps_view.end_edit(edit)
			else: # ST3
				if linetype == 'keymap':
					insert_space = insert_point
					line_ = line.lstrip()
					keymaps_view.run_command('append', {'characters':u'{0}'.format(' ' * (len(line)-len(line_)))})
					insert_point = insert_space + (keymaps_view.size() - insert_space)
					keymaps_view.run_command('append', {'characters':line_})
					rgn = sublime.Region(insert_point, keymaps_view.size())
					regions[(rgn.a, rgn.b)] = (rgn, data)
				else: # 'header'
					keymaps_view.run_command('append', {'characters':u'\n\n' + line.center(LINE_SIZE) + u'\n'})
				keymaps_view.run_command('append', {'characters':u'\n'})

			keymaps_view.add_regions('keymaps', [v[0] for k, v in regions.items()], '')

		## Store {Region : data} map in settings
		## TODO: Abstract this out to a storage class Storage.get(region) ==> data dict
		## Region() cannot be stored in settings, so convert to a primitive type
		# d_ = regions
		d_ = dict(('{0},{1}'.format(k[0], k[1]), v[1]) for k, v in regions.items())
		keymaps_view.settings().set('keymap_regions', d_)

		## Set syntax and settings
		keymaps_view.set_syntax_file('Packages/' + MY_NAME + '/cheat_sheet.hidden-tmLanguage')
		keymaps_view.settings().set('line_padding_bottom', 2)
		keymaps_view.settings().set('line_padding_top', 2)
		keymaps_view.settings().set('word_wrap', False)
		keymaps_view.settings().set('command_mode', True)
		self.window.focus_view(keymaps_view)


class FindKeymapRenderer(object):

	def __init__(self, settings, window, keymap_counter):
		self.settings = settings
		self.window = window
		self.keymap_counter = keymap_counter


	def format(self, packages):
		key_func = lambda m: m['package']
		packages = sorted(packages, key=key_func)
		myKeymaps = {}

		for package, matches in groupby(packages, key=key_func):
			matches = list(matches)
			if matches:

				for m in matches:
					keys = ''
					for key_token in m['keys']:
						keys = keys + u'[ ' + ' '.join(key_token) + u' ]'
					if self.settings['show_pretty_keys']:
						d = PRETTY_KEYS
						pattern = re.compile(r'\b(' + '|'.join(re.escape(key) for key in d.keys()) + r')\b')
						keys = pattern.sub(lambda x: d[x.group()], keys)
					args = m.get('args')
					if not args:
						args = None
					yield (package, keys, m['command'], args, m['caption'])


	def render(self, keymaps):
		self.keymaps = keymaps
		window = sublime.active_window()
		self.panel_items = []

		## Keymap sections
		for package, keys, command, args, caption in keymaps:
			self.panel_items.append([caption, keys + u' (' + package + u')'])

		# show_quick_panel(items, on_done, <flags>, <selected_index>, <on_highlighted>)
		window.show_quick_panel(self.panel_items, self.runcommand, sublime.MONOSPACE_FONT)


	def runcommand(self, idx):
		if idx == -1: return
		try:
			self.window.run_command(self.keymaps[idx][2], self.keymaps[idx][3])
		except Exception:
			pass


class WorkerThread(threading.Thread):

	def __init__(self, extractor, renderer):
		self.extractor = extractor
		self.renderer = renderer
		threading.Thread.__init__(self)


	def run(self):
		## Extract in this thread
		keymaps = self.extractor.extract()
		rendered = list(self.renderer.format(keymaps))

		## Render in main thread
		def render():
			self.renderer.render(rendered)

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

		## NOTE: numbers stored in settings are coerced to floats or longs
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
		keymap = self.view.substr(line)
		begin = len(keymap) - len(keymap.lstrip())
		return sublime.Region(line.a + begin, line.b)


	def run(self, edit):
		if not self.view.settings().get('keymap_regions'):
			return
		## get selected line
		pos = self.view.sel()[0].end()
		keymap = self.get_keymaps_region(pos)
		if pos == 0 or keymap.empty():
			sublime.error_message(MY_NAME + ':\n\nSelect some line first!')
			return
		self.highlight(keymap)

		## Region returned from mouse event is different(?) from the region of keyboard event,
		## so we fix it by forcing region.b = region.a
		data = self.view.settings().get('keymap_regions')['{0},{1}'.format(keymap.a, keymap.b)]

		self.log.debug(u'Goto keymap at {package}'.format(**data))
		## Open file for edit
		find_keymap(self.view, data)
