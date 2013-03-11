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

import android.accounts.Account;
import android.accounts.AccountManager;
import android.accounts.AccountManagerCallback;
import android.accounts.AccountManagerFuture;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;

import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.google.android.gcm.GCMRegistrar;

public class MainActivity extends SherlockFragmentActivity {

	public static final String TAG = "Keyring";
	public static final String SENDER_ID = "192076224105";

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

		ActionBar actionBar = getSupportActionBar();
		actionBar.setSubtitle("Something goes here");

		Intent upgradeIntent = versionUpgrade();
		if (upgradeIntent != null) {
			startActivity(upgradeIntent);
		}
	}

	private Intent versionUpgrade() {
		Intent intent = null;
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);

		if (prefs.contains("last_version")) {
			// TODO: check if we need to upgrade settings or something
		} else {
			// TODO: inject register/login flow here
			intent = new Intent(this, SettingsActivity.class);
		}

		return intent;
	}

	public void doGCMStuff() {
		GCMRegistrar.checkDevice(this);
		GCMRegistrar.checkManifest(this);

		final String regId = GCMRegistrar.getRegistrationId(this);
		if (regId.equals("")) {
			Log.v(TAG, "Registering");
			GCMRegistrar.register(this, SENDER_ID);
		} else {
			Log.v(TAG, "Already registered: " + regId);
		}

		AccountManager am = AccountManager.get(this);
		Account[] accounts = am.getAccountsByType("com.google");
		for (Account account : accounts) {
			Log.v(TAG, "Account: " + account.name + " (" + account.type + ")");
		}

		if (accounts.length > 0) {
			Account account = accounts[0];
			Bundle options = new Bundle();
			am.getAuthToken(
					account,
					"Keyring",
					options,
					this,
					new AccountManagerCallback<Bundle>() {
						@Override
						public void run(AccountManagerFuture<Bundle> result) {
							try {
								Bundle bundle = result.getResult();
								String token = bundle.getString(AccountManager.KEY_AUTHTOKEN);
								Intent intent = (Intent) bundle.get(AccountManager.KEY_INTENT);
								if (intent != null) {
									startActivityForResult(intent, 0);
									return;
								}
								Log.v(TAG, "onTokenAcquired: " + token);
							} catch(Exception e) {
								Log.v(TAG, "onTokenAcquired exception: " + e.toString());
							}
						}
					},
					new Handler() {
					}
					);

		}
    }
}
