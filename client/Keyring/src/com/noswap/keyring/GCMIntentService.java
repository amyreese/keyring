package com.noswap.keyring;

import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.google.android.gcm.GCMBaseIntentService;

public class GCMIntentService extends GCMBaseIntentService
{
	public static final String TAG = "Keyring";

	@Override
	public void onRegistered(Context context, String regId)
	{
		Log.v(TAG, "onRegistered: " + regId);
		// TODO: send regId to server
	}

	@Override
	public void onUnregistered(Context context, String regId)
	{
		Log.v(TAG, "onUnRegistered: " + regId);
		// TODO: remove regId from server
	}

	@Override
	public void onMessage(Context context, Intent intent)
	{
		Log.v(TAG, "onMessage: ");
	}

	@Override
	public void onError(Context context, String errorId)
	{
		Log.v(TAG, "onError: " + errorId);
	}

	//@Override
	//public void onRecoverableError(Context context, String errorId)
	//{
	//}
}

