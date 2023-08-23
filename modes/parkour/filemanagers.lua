local filemanagers = {
	["20"] = FileManager.new({
		type = "dictionary",
		map = {
			{
				name = "maps",
				type = "array",
				objects = {
					type = "number"
				}
			},
			{
				name = "ranks",
				type = "dictionary",
				objects = {
					type = "number"
				}
			},
			-- commented because the file is missing migration
			-- {
			-- 	name = "map_polls",
			-- 	type = "array",
			-- 	objects = {
			-- 		type = "number"
			-- 	}
			-- },
			{
				name = "chats",
				type = "dictionary",
				map = {
					{
						name = "mod",
						type = "string",
						length = 10
					},
					{
						name = "mapper",
						type = "string",
						length = 10
					}
				}
			}
		}
	}):disableValidityChecks():prepare(),

	["21"] = FileManager.new({
		type = "dictionary",
		map = {
			{
				name = "ranking",
				type = "array",
				objects = {
					type = "array",
					map = {
						{
							type = "number"
						},
						{
							type = "string",
						},
						{
							type = "number"
						},
						{
							type = "string",
							length = 2
						}
					}
				}
			},
			{
				name = "weekly",
				type = "dictionary",
				map = {
					{
						name = "ranks",
						type = "array",
						objects = {
							type = "array",
							map = {
								{
									type = "number"
								},
								{
									type = "string",
								},
								{
									type = "number"
								},
								{
									type = "string",
									length = 2
								}
							}
						}
					},
					{
						name = "ts",
						type = "string"
					},
					{
						name = "wl",
						type = "dictionary",
						objects = {
							type= "boolean"
						}
					}
				}
			}
		}
	}):disableValidityChecks():prepare(),

	["23"] = SanctionFileManager,
}