"""Roblox sword arena game script.

This file stores the Roblox Lua code in a Python text file so it can live alongside
other project files. Copy the Lua script from the triple-quoted string below and
paste it into a Script under ServerScriptService in Roblox Studio.
"""

ROBLOX_LUA = '''
-- Sword Arena Game
-- Paste into ServerScriptService

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local ARENA_SIZE = 80
local STARTING_WAVE = 1

local currentWave = STARTING_WAVE
local enemies = {}

local function clearFolder(name)
	local folder = workspace:FindFirstChild(name)
	if folder then
		folder:Destroy()
	end
end

local function randomArenaPosition()
	return Vector3.new(
		math.random(-ARENA_SIZE / 2 + 8, ARENA_SIZE / 2 - 8),
		3,
		math.random(-ARENA_SIZE / 2 + 8, ARENA_SIZE / 2 - 8)
	)
end

local function createArena()
	clearFolder("SwordArena")
	clearFolder("EnemyFolder")

	local arenaFolder = Instance.new("Folder")
	arenaFolder.Name = "SwordArena"
	arenaFolder.Parent = workspace

	local enemyFolder = Instance.new("Folder")
	enemyFolder.Name = "EnemyFolder"
	enemyFolder.Parent = workspace

	local floor = Instance.new("Part")
	floor.Name = "Floor"
	floor.Size = Vector3.new(ARENA_SIZE, 1, ARENA_SIZE)
	floor.Position = Vector3.new(0, 0, 0)
	floor.Anchored = true
	floor.Material = Enum.Material.Slate
	floor.Color = Color3.fromRGB(20, 20, 30)
	floor.Parent = arenaFolder

	for _, data in ipairs({
		{Vector3.new(0, 6, ARENA_SIZE / 2), Vector3.new(ARENA_SIZE + 10, 12, 2)},
		{Vector3.new(0, 6, -ARENA_SIZE / 2), Vector3.new(ARENA_SIZE + 10, 12, 2)},
		{Vector3.new(ARENA_SIZE / 2, 6, 0), Vector3.new(2, 12, ARENA_SIZE + 10)},
		{Vector3.new(-ARENA_SIZE / 2, 6, 0), Vector3.new(2, 12, ARENA_SIZE + 10)},
	}) do
		local wall = Instance.new("Part")
		wall.Size = data[2]
		wall.Position = data[1]
		wall.Anchored = true
		wall.Material = Enum.Material.SmoothPlastic
		wall.Color = Color3.fromRGB(80, 90, 110)
		wall.Parent = arenaFolder
	end

	local spawnPad = Instance.new("Part")
	spawnPad.Name = "SpawnPad"
	spawnPad.Size = Vector3.new(14, 1, 14)
	spawnPad.Position = Vector3.new(0, 1, 0)
	spawnPad.Anchored = true
	spawnPad.Material = Enum.Material.Neon
	spawnPad.Color = Color3.fromRGB(72, 190, 120)
	spawnPad.Parent = arenaFolder
end

local function setupLeaderstats(player)
	local leaderstats = player:FindFirstChild("leaderstats")
	if leaderstats then
		leaderstats:Destroy()
	end

	leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	leaderstats.Parent = player

	local score = Instance.new("IntValue")
	score.Name = "Score"
	score.Value = 0
	score.Parent = leaderstats

	local wave = Instance.new("IntValue")
	wave.Name = "Wave"
	wave.Value = 1
	wave.Parent = leaderstats

	local health = Instance.new("IntValue")
	health.Name = "Health"
	health.Value = 100
	health.Parent = leaderstats
end

local function giveSword(player)
	local existing = player.Backpack:FindFirstChild("BattleSword")
	if existing then
		existing:Destroy()
	end

	local tool = Instance.new("Tool")
	tool.Name = "BattleSword"
	tool.RequiresHandle = true

	local handle = Instance.new("Part")
	handle.Name = "Handle"
	handle.Size = Vector3.new(0.5, 4, 0.5)
	handle.Material = Enum.Material.Metal
	handle.Color = Color3.fromRGB(180, 180, 180)
	handle.CanCollide = false
	handle.Parent = tool

	local blade = Instance.new("Part")
	blade.Name = "Blade"
	blade.Size = Vector3.new(0.5, 2, 0.8)
	blade.Material = Enum.Material.Neon
	blade.Color = Color3.fromRGB(120, 220, 255)
	blade.CanCollide = false
	blade.Parent = tool

	local weld = Instance.new("WeldConstraint")
	weld.Part0 = handle
	weld.Part1 = blade
	weld.Parent = tool

	tool.Parent = player.Backpack

	tool.Activated:Connect(function()
		local character = player.Character
		if not character then return end

		local root = character:FindFirstChild("HumanoidRootPart")
		local humanoid = character:FindFirstChildOfClass("Humanoid")
		if not root or not humanoid then return end

		for _, enemy in ipairs(enemies) do
			local enemyRoot = enemy:FindFirstChild("HumanoidRootPart")
			if enemyRoot then
				local distance = (enemyRoot.Position - root.Position).Magnitude
				local lookDir = (enemyRoot.Position - root.Position)
				local forward = root.CFrame.LookVector
				local dot = lookDir.Unit:Dot(forward)

				if distance <= 8 and dot > 0.2 then
					local enemyHumanoid = enemy:FindFirstChildOfClass("Humanoid")
					if enemyHumanoid and enemyHumanoid.Health > 0 then
						enemyHumanoid:TakeDamage(35)

						if enemyHumanoid.Health <= 0 then
							local leaderstats = player:FindFirstChild("leaderstats")
							if leaderstats then
								local score = leaderstats:FindFirstChild("Score")
								if score then
									score.Value += 10
								end
							end
						end
					end
				end
			end
		end
	end)
end

local function setupPlayer(player)
	setupLeaderstats(player)
	player.CharacterAdded:Connect(function(character)
		task.wait(0.2)
		local hrp = character:WaitForChild("HumanoidRootPart")
		hrp.CFrame = CFrame.new(0, 5, 0)

		local humanoid = character:WaitForChild("Humanoid")
		humanoid.WalkSpeed = 16

		task.wait(0.2)
		giveSword(player)
	end)
end

for _, player in ipairs(Players:GetPlayers()) do
	setupPlayer(player)
end

Players.PlayerAdded:Connect(function(player)
	setupPlayer(player)
end)

local function createEnemy(name, position)
	local enemyModel = Instance.new("Model")
	enemyModel.Name = name

	local root = Instance.new("Part")
	root.Name = "HumanoidRootPart"
	root.Size = Vector3.new(2, 2, 2)
	root.Position = position
	root.Anchored = false
	root.CanCollide = false
	root.Transparency = 1
	root.Parent = enemyModel

	local torso = Instance.new("Part")
	torso.Name = "Torso"
	torso.Size = Vector3.new(2, 3, 1)
	torso.Position = position + Vector3.new(0, 2, 0)
	torso.Color = Color3.fromRGB(255, 60, 60)
	torso.Material = Enum.Material.SmoothPlastic
	torso.Parent = enemyModel

	local head = Instance.new("Part")
	head.Name = "Head"
	head.Size = Vector3.new(2, 1.5, 2)
	head.Position = position + Vector3.new(0, 4.2, 0)
	head.Color = Color3.fromRGB(180, 50, 50)
	head.Material = Enum.Material.SmoothPlastic
	head.Parent = enemyModel

	local leftArm = Instance.new("Part")
	leftArm.Name = "Left Arm"
	leftArm.Size = Vector3.new(0.8, 2.5, 0.8)
	leftArm.Position = position + Vector3.new(-1.5, 2, 0)
	leftArm.Color = Color3.fromRGB(255, 60, 60)
	leftArm.Parent = enemyModel

	local rightArm = Instance.new("Part")
	rightArm.Name = "Right Arm"
	rightArm.Size = Vector3.new(0.8, 2.5, 0.8)
	rightArm.Position = position + Vector3.new(1.5, 2, 0)
	rightArm.Color = Color3.fromRGB(255, 60, 60)
	rightArm.Parent = enemyModel

	local leftLeg = Instance.new("Part")
	leftLeg.Name = "Left Leg"
	leftLeg.Size = Vector3.new(0.8, 2.8, 0.8)
	leftLeg.Position = position + Vector3.new(-0.6, -1.6, 0)
	leftLeg.Color = Color3.fromRGB(40, 40, 40)
	leftLeg.Parent = enemyModel

	local rightLeg = Instance.new("Part")
	rightLeg.Name = "Right Leg"
	rightLeg.Size = Vector3.new(0.8, 2.8, 0.8)
	rightLeg.Position = position + Vector3.new(0.6, -1.6, 0)
	rightLeg.Color = Color3.fromRGB(40, 40, 40)
	rightLeg.Parent = enemyModel

	local weldRoot = Instance.new("WeldConstraint")
	weldRoot.Part0 = root
	weldRoot.Part1 = torso
	weldRoot.Parent = enemyModel

	for _, part in ipairs({head, leftArm, rightArm, leftLeg, rightLeg}) do
		local weld = Instance.new("WeldConstraint")
		weld.Part0 = torso
		weld.Part1 = part
		weld.Parent = enemyModel
	end

	local humanoid = Instance.new("Humanoid")
	humanoid.Name = "EnemyHumanoid"
	humanoid.MaxHealth = 50 + currentWave * 15
	humanoid.Health = humanoid.MaxHealth
	humanoid.WalkSpeed = 8 + currentWave * 0.6
	humanoid.Parent = enemyModel

	local enemyFolder = workspace:FindFirstChild("EnemyFolder")
	if enemyFolder then
		enemyModel.Parent = enemyFolder
	end

	table.insert(enemies, enemyModel)
	return enemyModel
end

local function spawnWave()
	for _, enemy in ipairs(enemies) do
		if enemy and enemy.Parent then
			enemy:Destroy()
		end
	end
	enemies = {}

	local count = math.min(3 + currentWave, 12)
	for i = 1, count do
		createEnemy("Enemy" .. i, randomArenaPosition())
	end

	for _, player in ipairs(Players:GetPlayers()) do
		local leaderstats = player:FindFirstChild("leaderstats")
		if leaderstats then
			local waveValue = leaderstats:FindFirstChild("Wave")
			if waveValue then
				waveValue.Value = currentWave
			end
		end
	end
end

local function checkForWaveClear()
	local alive = false
	for _, enemy in ipairs(enemies) do
		local humanoid = enemy:FindFirstChildOfClass("Humanoid")
		if humanoid and humanoid.Health > 0 then
			alive = true
			break
		end
	end

	if not alive then
		currentWave += 1
		spawnWave()
	end
end

local function hurtPlayer(player, amount)
	local leaderstats = player:FindFirstChild("leaderstats")
	if not leaderstats then return end

	local health = leaderstats:FindFirstChild("Health")
	if not health then return end

	health.Value = math.max(0, health.Value - amount)
	if health.Value <= 0 then
		local character = player.Character
		if character then
			local hrp = character:FindFirstChild("HumanoidRootPart")
			if hrp then
				hrp.CFrame = CFrame.new(0, 5, 0)
			end
		end
		health.Value = 100
		local score = leaderstats:FindFirstChild("Score")
		if score then
			score.Value = math.max(0, score.Value - 20)
		end
	end
end

local function chaseEnemies(dt)
	for _, enemy in ipairs(enemies) do
		if not enemy or not enemy.Parent then
			continue
		end

		local humanoid = enemy:FindFirstChildOfClass("Humanoid")
		local root = enemy:FindFirstChild("HumanoidRootPart")

		if humanoid and root and humanoid.Health > 0 then
			local nearestPlayer = nil
			local nearestDistance = math.huge

			for _, player in ipairs(Players:GetPlayers()) do
				local character = player.Character
				if character then
					local playerRoot = character:FindFirstChild("HumanoidRootPart")
					if playerRoot then
						local distance = (playerRoot.Position - root.Position).Magnitude
						if distance < nearestDistance then
							nearestDistance = distance
							nearestPlayer = player
						end
					end
				end
			end

			if nearestPlayer then
				local targetCharacter = nearestPlayer.Character
				local targetRoot = targetCharacter and targetCharacter:FindFirstChild("HumanoidRootPart")
				if targetRoot then
					local direction = (targetRoot.Position - root.Position)
					local distance = direction.Magnitude
					if distance > 0 then
						direction = direction.Unit
					end

					root.CFrame = root.CFrame + CFrame.new(direction * (humanoid.WalkSpeed * dt)).Position

					if distance < 3 then
						hurtPlayer(nearestPlayer, 12 * dt * 60)
					end
				end
			end
		end
	end
end

createArena()
for _, player in ipairs(Players:GetPlayers()) do
	setupPlayer(player)
end
spawnWave()

RunService.Heartbeat:Connect(function(dt)
	chaseEnemies(dt)
	checkForWaveClear()
end)
'''

if __name__ == "__main__":
    print(ROBLOX_LUA)
