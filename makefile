
test-client: client/Keyring/bin/Keyring-debug.apk
	adb install -r $<

client/Keyring/bin/Keyring-debug.apk: client/Keyring
	cd $< && ant debug

clean:
	rm -rf client/Keyring/bin/
