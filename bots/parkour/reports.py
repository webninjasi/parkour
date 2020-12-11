"""
Handles reports
"""

from parkour.env import env
from parkour.utils import normalize_name
import asyncio
import aiotfm
import time


class Reports(aiotfm.Client):
	def __init__(self, *args, **kwargs):
		self.rep_id = 0
		self.reports = {}
		self.reported = []
		self.reporters = []

		super().__init__(*args, **kwargs)

		self.loop.create_task(self.check_reports())

	async def check_reports(self):
		while not self.main.open:
			await asyncio.sleep(3.0)

		while self.main.open:
			now = time.time()
			to_remove = []

			for report, data in self.reports.items():
				# reporter, reported, sent to discord,
				# discord date, expiration date

				if not data[2] and now >= data[3]:
					data[2] = True
					await self.report_discord(report)

				elif now >= data[4]: # expired
					self.reported.remove(data[1])
					to_remove.append(report)
					await self.mod_chat.channel.send(
						"Report id {} has expired.".format(report)
					)

			for report in to_remove:
				del self.reports[report]

			await asyncio.sleep(30.0)

	async def report_discord(self, report):
		reporter, reported = self.reports[report][:2]

		file = await self.load_player_file(reported)
		if file is None:
			room = "unknown"
		else:
			room = file["room"]

		await self.send_channel(
			env.report_channel,
			"@everyone `{}` reported `{}` (room: `{}`, report id: `{}`). "
			"Connect to the game and use the handle command in modchat."
			.format(reporter, reported, room, report)
		)

	def report_cooldown(self, name):
		reports = 0
		remove_until = -1
		now = time.time()

		for index, (expire, reporter) in enumerate(self.reporters):
			if now >= expire:
				remove_until = index

			elif reporter == name:
				reports += 1

		if remove_until >= 0:
			del self.reporters[:remove_until + 1]

		if reports >= 2:
			return True
		return False

	async def on_channel_command(self, channel, name, author, ranks, cmd, args):
		if name == "mod":
			if cmd == "handle":
				if (not ranks["admin"]
					and not ranks["mod"]
					and not ranks["trainee"]):
					return True

				if not args or not args[0].isdigit():
					await channel.send("Usage: .handle [id] (silent?)")
					return True

				rep_id = int(args[0])
				if len(args) > 1:
					silent = args[1].lower() in ("silent", "silence", "s")
				else:
					silent = False

				if rep_id not in self.reports:
					return await channel.send("Report id {} not found".format(rep_id))

				report = self.reports[rep_id]
				del self.reports[rep_id]

				file = await self.load_player_file(report[1])
				if file is None:
					extra = "Could not get reported player information."
				else:
					extra = "Sent you the player's room in whispers."
					await self.whisper(
						author,
						"{}'s room: {}".format(report[1], file["room"])
					)

				await channel.send(
					"{} will be handling the report {}. {}"
					.format(author, rep_id, extra)
				)

				if not silent:
					await self.whisper(
						report[0],
						"A parkour moderator is now handling your report."
					)

			else:
				return False
		else:
			return False
		return True

	async def on_whisper_command(self, whisper, author, ranks, cmd, args):
		if await super().on_whisper_command(
			whisper, author, ranks, cmd, args
		):
			return True

		if cmd == "report":
			# Argument check
			if not args:
				return await whisper.reply("Usage: .report Username#0000")

			reported = normalize_name(args[0])
			if reported == author:
				return await whisper.reply("Why are you trying to report yourself?")

			pid, name, online = await self.get_player_info(reported)
			if name is None or not online:
				return await whisper.reply("That player ({}) is not online.".format(reported))

			await whisper.reply("Your report of the player {} will be handled shortly.".format(reported))

			# Player information check
			if self.report_cooldown(author):
				return

			if reported in self.reported:
				return

			file = await self.load_player_file(author, online_check=False)
			if file is None or not file["report"]:
				return

			file = await self.load_player_file(reported, online_check=False)
			if file is None:
				return

			now = self.tfm_time()
			if now < file.get("killed", 0):
				return

			ban = file.get("banned", 0)
			if ban == 2 or now < ban:
				return

			# Create report
			report = self.rep_id
			self.rep_id += 1

			online = len(self.mod_chat.players) - 1
			now = time.time()
			self.reports[report] = [
				author, reported, online == 0,
				now + 60 * 5, now + 60 * 30
			]
			self.reported.append(reported)
			self.reporters.append((now + 60 * 5, author))

			if online == 0:
				await self.report_discord(report)

			else:
				await self.mod_chat.channel.send(
					"{} reported {} (report id: {}) (room: {}) "
					"(use the handle command here before handling it)"
					.format(author, reported, report, file["room"])
				)

		else:
			return False
		return True