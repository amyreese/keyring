client_sources=$(shell find Keyring -name '*.java' -or -name '*.xml')\
			   Keyring/ant.properties\
			   Keyring/project.properties\
			   Keyring/proguard-project.txt

%.xml:

debug: debug-client
	adb logcat -c
	adb logcat -s AndroidRuntime:E Keyring:V

debug-client: Keyring/bin/Keyring-debug.apk
	adb install -r $<

Keyring/bin/Keyring-debug.apk: $(client_sources)
	cd Keyring && ant debug

clean:
	rm -rf Keyring/bin/ Keyring/gen/

fresh: clean debug
