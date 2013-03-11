/**
 * Copyright 2013 John Reese
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.noswap.keyring;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.Preference;
import android.preference.PreferenceScreen;
import android.preference.PreferenceManager;
import android.util.Log;

import com.actionbarsherlock.app.SherlockPreferenceActivity;

public class SettingsActivity extends SherlockPreferenceActivity {

	public static final String TAG = "Keyring";

	@Override
	public void onCreate(Bundle savedState) {
		super.onCreate(savedState);
		addPreferencesFromResource(R.xml.preferences);

		updateSummaries();
	}

	@Override
	public boolean onPreferenceTreeClick(PreferenceScreen screen, Preference pref) {
		boolean retval = super.onPreferenceTreeClick(screen, pref);
		Log.v(TAG, "clicked on preference " + pref.getKey() + ", retval " + (retval ? "true" : "false"));

		updateSummaries();
		return true;
	}

	private void updateSummaries() {
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);

		findPreference("email").setSummary(prefs.getString("email", "n/a"));
		findPreference("device_name").setSummary(prefs.getString("device_name", "n/a"));
	}

}
