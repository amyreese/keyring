sources=$(shell find client/Keyring -name '*.java' -or -name '*.xml')

debug: debug-client
	adb logcat -c
	adb logcat -s AndroidRuntime:E Keyring:V

debug-client: client/Keyring/bin/Keyring-debug.apk
	adb install -r $<

client/Keyring/bin/Keyring-debug.apk: client/Keyring $(sources)
	cd $< && ant debug

clean:
	rm -rf client/Keyring/bin/
