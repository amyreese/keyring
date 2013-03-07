client_sources=$(shell find client/Keyring -name '*.java' -or -name '*.xml')\
			   client/Keyring/build.xml\
			   client/Keyring/ant.properties\
			   client/Keyring/project.properties\
			   client/Keyring/proguard-project.txt

debug: debug-client
	adb logcat -c
	adb logcat -s AndroidRuntime:E Keyring:V

debug-client: client/Keyring/bin/Keyring-debug.apk
	adb install -r $<

client/Keyring/bin/Keyring-debug.apk: client/Keyring $(client_sources)
	cd $< && ant debug

clean:
	rm -rf client/Keyring/bin/
