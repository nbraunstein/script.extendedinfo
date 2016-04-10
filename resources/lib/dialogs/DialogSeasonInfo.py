# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details
import xbmcgui

from .. import Utils
from kodi65 import addon
from .. import TheMovieDB as tmdb
from .. import ImageTools
from DialogBaseInfo import DialogBaseInfo
from ..WindowManager import wm
from ActionHandler import ActionHandler

ID_LIST_YOUTUBE = 350
ID_LIST_CREW = 750
ID_LIST_ACTORS = 1000
ID_LIST_EPISODES = 2000
ID_LIST_VIDEOS = 1150
ID_LIST_IMAGES = 1250
ID_LIST_BACKDROPS = 1350
ID_CONTROL_PLOT = 132

ch = ActionHandler()


def get_window(window_type):

    class DialogSeasonInfo(DialogBaseInfo, window_type):

        def __init__(self, *args, **kwargs):
            super(DialogSeasonInfo, self).__init__(*args, **kwargs)
            self.type = "Season"
            self.tvshow_id = kwargs.get('id')
            data = tmdb.extended_season_info(tvshow_id=self.tvshow_id,
                                             season_number=kwargs.get('season'))
            if not data:
                return None
            self.info, self.data = data
            if "dbid" not in self.info:  # need to add comparing for seasons
                poster = Utils.get_file(url=self.info.get("poster", ""))
                self.info.set_art("poster", poster)
            self.info.update_properties(ImageTools.blur(self.info.get_art("poster")))
            self.listitems = [(ID_LIST_ACTORS, self.data["actors"]),
                              (ID_LIST_CREW, self.data["crew"]),
                              (ID_LIST_EPISODES, self.data["episodes"]),
                              (ID_LIST_VIDEOS, self.data["videos"]),
                              (ID_LIST_IMAGES, self.data["images"]),
                              (ID_LIST_BACKDROPS, self.data["backdrops"])]

        def onInit(self):
            self.get_youtube_vids("%s %s tv" % (self.info["tvshowtitle"], self.info['title']))
            super(DialogSeasonInfo, self).onInit()

        def onClick(self, control_id):
            super(DialogSeasonInfo, self).onClick(control_id)
            ch.serve(control_id, self)

        @ch.click(ID_LIST_CREW)
        @ch.click(ID_LIST_ACTORS)
        def open_actor_info(self, control_id):
            wm.open_actor_info(prev_window=self,
                               actor_id=self.FocusedItem(control_id).getProperty("id"))

        @ch.click(ID_LIST_EPISODES)
        def open_episode_info(self, control_id):
            info = self.FocusedItem(control_id).getVideoInfoTag()
            wm.open_episode_info(prev_window=self,
                                 tvshow=self.info["tvshowtitle"],
                                 tvshow_id=self.tvshow_id,
                                 season=info.getSeason(),
                                 episode=info.getEpisode())

        @ch.click(ID_CONTROL_PLOT)
        def open_text(self, control_id):
            xbmcgui.Dialog().textviewer(heading=addon.LANG(32037),
                                        text=self.info.get_info("plot"))

        @ch.click(ID_LIST_YOUTUBE)
        @ch.click(ID_LIST_VIDEOS)
        def play_youtube_video(self, control_id):
            wm.play_youtube_video(youtube_id=self.FocusedItem(control_id).getProperty("youtube_id"),
                                  listitem=self.FocusedItem(control_id),
                                  window=self)

    return DialogSeasonInfo
