local packets = {}

packets.rooms = {
  crash = 0,
  hourly_record = 3,
  weekly_reset = 4,
  pw_response = 5,
  command_log = 7,
  poll_answer = 8,
  title_logs = 9,
  kill_logs = 10,
  report = 11,
  ban_logs = 12,
  update_error = 13,
  lock_fixed = 14,
  prev_kill = 15,
  skip_map = 16,
}

packets.bots = {
  join = 0,
  game_update = 1,
  update_pdata = 2,
  --ban = 3,
  announce = 4,
  cm_announce = 5,
  pw_request = 6,
  room_announce = 7,
  change_lock = 8,
  remote_command = 9,
}
