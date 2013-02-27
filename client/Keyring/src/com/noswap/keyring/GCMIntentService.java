package com.noswap.keyring;

import com.google.android.gcm.GCMBaseIntentService;
import android.content.Context;
import android.content.Intent;

public class GCMIntentService extends GCMBaseIntentService
{
	@Override
	public void onRegistered(Context context, String regId)
	{
		// TODO: send regId to server
	}

	@Override
	public void onUnregistered(Context context, String regId)
	{
		// TODO: remove regId from server
	}

	@Override
	public void onMessage(Context context, Intent intent)
	{
		// Do something with the message
	}

	@Override
	public void onError(Context context, String errorId)
	{
	}

	//@Override
	//public void onRecoverableError(Context context, String errorId)
	//{
	//}
}

