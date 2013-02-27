
test-client:
	cd client/Keyring && ant debug && adb install -r bin/Keyring-debug.apk
