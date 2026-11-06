tool_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_cost",
            "description": "查询成本",
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "产品SKU"},
                },
                "required": ["sku"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_commission_rate",
            "description": "查询佣金率",
            "parameters": {
                "type": "object",
                "properties": {
                    "store_id": {"type": "string", "description": "店铺ID"},
                },
                "required": ["store_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "查询汇率",
            "parameters": {
                "type": "object",
                "properties": {
                    "store_id": {"type": "string", "description": "店铺ID"},
                },
                "required": ["store_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_filter_csv",
            "description": "读取CSV文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "文件路径"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_to_new_file",
            "description": "保存到新文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "文件路径"},
                },
                "required": ["file_path"],
            },
        },
    },
]