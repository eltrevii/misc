import pymem as pmm, win32api as wapi, time as t

# offsets
LOCAL_PLAYER	= 14596508
FORCE_JUMP		= 86756744
HEALTH			= 256
FLAGS			= 260

def bhop() -> None:
	pm = pmm.Pymem('csgo.exe')

	# get module addr
	for module in list(pm.list_modules()):
		if module.name == 'client.dll':
			client = module.lpBaseOfDll

	# h4xx loop
	while True:
		t.sleep(0.01)

		# space bar
		if not wapi.GetAsyncKeyState(0x20):
			continue

		local_player: int = pm.read_uint(client + LOCAL_PLAYER)

		if not local_player:
			continue

		# is alive(?)
		if not pm.read_int(local_player + HEALTH):
			continue

		# is on ground(?)
		if pm.read_uint(local_player + FLAGS) & 1 << 0:
			pm.write_uint(client + FORCE_JUMP, 6)
			time.sleep(0.01)
			pm.write_uint(client + FORCE_JUMP, 4)

if __name__ == '__main__':
	bhop()