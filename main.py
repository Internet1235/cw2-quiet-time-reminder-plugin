"""
Test
A Class Widgets plugin.
"""

from ClassWidgets.SDK import CW2Plugin, PluginAPI
from datetime import datetime
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class Plugin(CW2Plugin):
    def __init__(self, api: PluginAPI):
        super().__init__(api)
        # 若要引用插件目录的内容，需在目录前添加插件的工作目录：
        self.plugin_dir = Path(__file__).parent
        self.notified_times = set()  # 用于记录已经发送通知的时间点
        self.current_date = datetime.now().date()  # 记录当前日期
        # 请在此导入第三方库 / Import third-party libraries here

    def update(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        today = now.date()

        # 如果日期变化（即到了第二天），清空已通知的时间点
        if today != self.current_date:
            self.notified_times.clear()
            self.current_date = today  # 更新当前日期

        if current_time in ['18:45', '20:10'] and current_time not in self.notified_times:
            self.notification_provider.push(
                level=1,  # 自定义通知
                title='静班提醒',
                # content=f'静班时间到！当前时间：{current_time}',
                message=f'现在是晚修时间，请保持安静！！！当前时间: {current_time}',
                duration=150000,  # 通知持续时间（毫秒）
                closable=True
            )
            self.notified_times.add(current_time)

        if current_time == '15:20' and current_time not in self.notified_times:
            self.notification_provider.push(
                level=1,  # 自定义通知
                title='上课',
                #title='静班提醒',
                #subtitle='',
                # content=f'静班时间到！当前时间：{current_time}',
                #content=f'现在是晚修时间，请保持安静！！！\n当前时间: {current_time}',
                message="眼保健操",
                duration=1500, # 通知持续时间（毫秒）
                closable=True
            )
            self.notified_times.add(current_time)

        if current_time == '14:20' and current_time not in self.notified_times:
            self.notification_provider.push(
                level=1,  # 自定义通知
                title='上课',
                #title='静班提醒',
                #subtitle='',
                # content=f'静班时间到！当前时间：{current_time}',
                #content=f'现在是晚修时间，请保持安静！！！\n当前时间: {current_time}',
                message="练字",
                duration=1500,  # 通知持续时间（毫秒）
                closable=True
            )
            self.notified_times.add(current_time)

        if current_time == '07:30' and current_time not in self.notified_times:
            self.notification_provider.push(
                level=1,  # 自定义通知
                title='上课',
                #title='静班提醒',
                #subtitle='',
                # content=f'静班时间到！当前时间：{current_time}',
                #content=f'现在是晚修时间，请保持安静！！！\n当前时间: {current_time}',
                message="早读",
                duration=1500,  # 通知持续时间（毫秒）
                closable=True
            )
            self.notified_times.add(current_time)

        if current_time == '12:45' and current_time not in self.notified_times:
            self.notification_provider.push(
                level=1,  # 自定义通知
                title='离班提醒',
                # subtitle='',
                # content=f'静班时间到！当前时间：{current_time}',
                message=f'该回寝睡觉了，小心迟到扣分！当前时间: {current_time}',
                duration=1500000,  # 通知持续时间（毫秒）
                closable=True
            )
            self.notified_times.add(current_time)

            self._player.setSource(QUrl.fromLocalFile(f"{self.plugin_dir}/audios/leave_classroom_reminder.mp3"))
            self._player.play()

    def on_load(self):
        super().on_load()
        print(f"Test loaded")
        
        self._player = QMediaPlayer()
        self._audio_output = QAudioOutput()
        self._player.setAudioOutput(self._audio_output)

        self.notification_provider = self.api.notification.register_provider(
            provider_id=self.pid,
            name="静班提醒",
            icon="icon.png"
		)

        self.api.runtime.updated.connect(self.update)

    def on_unload(self):
        print(f"Test unloaded")
