// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class RL_game : ModuleRules
{
	public RL_game(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "Paper2D" });
	}
}
