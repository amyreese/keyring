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
import android.preference.PreferenceManager;
import android.util.Log;

import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentManager;

import com.actionbarsherlock.app.ActionBar;
import com.actionbarsherlock.app.SherlockFragment;
import com.actionbarsherlock.app.SherlockFragmentActivity;
import com.actionbarsherlock.view.Menu;
import com.actionbarsherlock.view.MenuItem;
import com.actionbarsherlock.view.MenuInflater;
import com.google.android.gcm.GCMRegistrar;

public class MainActivity extends SherlockFragmentActivity {

	public static final String TAG = "Keyring";
	public static final String SENDER_ID = "192076224105";

	public boolean menuEnabled = true;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

		ActionBar actionBar = getSupportActionBar();
		actionBar.setTitle(R.string.app_name);

		FragmentManager manager = getSupportFragmentManager();
		Fragment fragment = manager.findFragmentById(R.id.main_container);

		Intent upgradeIntent = versionUpgrade();
		if (upgradeIntent != null) {
			startActivity(upgradeIntent);
		} else {
			if (fragment == null) {
				manager.beginTransaction()
					.add(R.id.main_container, new LoginFragment())
					.commit();
			}
		}
	}

	@Override
	public void onResume() {
		super.onResume();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		Log.v(TAG, "onCreateOptionsMenu() -- menuEnabled: " + (menuEnabled ? "true" : "false"));
		if (menuEnabled) {
			getSupportMenuInflater().inflate(R.menu.main, menu);
		}
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		int id = item.getItemId();
		if (id == R.id.menu_main_settings) {
			startActivity(new Intent(this, SettingsActivity.class));
		} else if (id == R.id.menu_main_about) {
			// TODO: About screen
		} else {
			Log.e(TAG, "Selected unknown menu item id " + id);
		}
		return true;
	}

	private Intent versionUpgrade() {
		Intent intent = null;
		SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);

		if (prefs.contains("last_version")) {
			// TODO: check if we need to upgrade settings or something
		} else {
			// TODO: inject register/login flow here
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
