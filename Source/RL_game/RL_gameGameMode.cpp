// Copyright Epic Games, Inc. All Rights Reserved.

#include "RL_gameGameMode.h"
#include "RL_gameCharacter.h"

ARL_gameGameMode::ARL_gameGameMode()
{
	// Set default pawn class to our character
	DefaultPawnClass = ARL_gameCharacter::StaticClass();	
}
