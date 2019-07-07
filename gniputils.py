CMD_ALL = 'GNIP_DUMPALL'
CMD_TREE = 'GNIP_DUMPTREE'


def register(trg):
    trg._parent.log_message('Registering UserAction command:%s from:%s' % (CMD_ALL, __file__))
    # Add method from this file to the ClyphXUserActions class
    type(trg).gnip_dumpall = dumpall_cmd
    # Register method with ClyphX command
    trg._action_dict[CMD_ALL] = 'gnip_dumpall'

    trg._parent.log_message('Registering UserAction command:%s from:%s' % (CMD_TREE, __file__))
    # Add method from this file to the ClyphXUserActions class
    type(trg).gnip_dumptree = dumptree_cmd
    # Register method with ClyphX command
    trg._action_dict[CMD_TREE] = 'gnip_dumptree'


#################### ClyphXUserActions
def dumpall_cmd(self, track, args):
    """<CMD> - dump info about song, view, tracks and first track to Log.txt
    <CMD> true - dump same info but with functions shown as well"""
    show_funcs = args.lower() == 'true'
    txt = ''
    txt += '\n' + _dumpobj(self.song(), show_funcs)
    txt += '\n' + _dumpobj(self.song().view, show_funcs)
    txt += '\n' + _dumpobj(self.song().tracks, show_funcs)
    txt += '\n' + _dumpobj(self.song().tracks[0], show_funcs)
    self._parent.log_message(txt)

def dumptree_cmd(self, track, args):
    """Dump basic song, song view, track, clip info"""
    t = '\n'
    song = self.song()
    t += 'Song: length:%.f cur:%.f playing:%s tempo:%.f\n' % (
    song.song_length, song.current_song_time, song.is_playing, song.tempo)
    sel_trk = song.view.selected_track
    sel_scene = song.view.selected_scene
    hilited_clip = '<empty slot>' if song.view.highlighted_clip_slot.clip is None else song.view.highlighted_clip_slot.clip.name
    t += 'Song view: selTrk:%s selScene:%s selClip:%s\n' % (sel_trk.name, sel_scene.name, hilited_clip)
    for track in song.tracks:
        t += '    track %s\n' % track.name
        for slot in track.clip_slots:
            tag = '' if slot.clip is None else slot.clip.name
            t += '        clipslot %s\n' % tag

    self._parent.log_message(t)


#################### Supporting code
def _make_member_desc(member_name, member):
    return '{} <{}>'.format(member_name, type(member).__name__)


def _dumpobj(obj, show_callables=False):
    '''A debugging function that prints out the names and values of all the
    members of the given object.  Very useful for inspecting objects in
    interactive sessions'''
    txt = 'TYPE: %s\n' % type(obj).__name__

    members = {}
    for name in dir(obj):
        try:
            members[name] = getattr(obj, name)
        except Exception as e:
            members[name] = 'EXCEPTION getting value: %s - %s' % (type(e), str(e))

    members = {name: member for name, member in members.items()
               if name not in ('__builtins__', '__doc__')}
    members = {name: member for name, member in members.items()
               if not name.startswith('__') and not name.endswith('__')}
    if not show_callables:
        members = {name: member for name, member in members.items()
                   if not callable(member)}
    if len(members) == 0:
        txt += '  <EMPTY>\n'
        return txt
    max_desc_len = max([len(_make_member_desc(k, v)) for k, v in members.items()])

    items = list(members.items())
    items.sort()
    for name, member in items:
        member_desc = _make_member_desc(name, member)
        txt += '  {} = {}\n'.format(member_desc.ljust(max_desc_len), member)

    return txt
