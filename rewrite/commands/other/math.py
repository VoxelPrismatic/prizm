info = {
    "name": "math",
    "description": "Math commands",
    "type": 2,
    "id": "math",
    "options": [
        {
            "name": "stats",
            "description": "Gives you the statistics about some data",
            "type": 1,
            "options": []
        },
        {
            "name": "simplify",
            "description": "Simplifies an equation",
            "type": 1,
            "options": [
                {
                    "name": "equation",
                    "description": "The equation to simplify",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "calc",
            "description": "Calculate stuff",
            "type": 1,
            "options": [
                {
                    "name": "equation",
                    "description": "The equation to solve",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "radians",
                    "description": "Whether or not to use radians. Degrees by default",
                    "type": 5,
                    "required": False
                }
            ]
        },
        {
            "name": "fraction",
            "description": "Simplifies a fraction or ratio",
            "type": 1,
            "options": [
                {
                    "name": "x",
                    "description": "x in x/y or x:y",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "y",
                    "description": "y in x/y or x:y",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "quadratic",
            "description": "Solves the quadratic formula",
            "type": 1,
            "options": [
                {
                    "name": "a",
                    "description": "(-b ± √(b² - 4ac))/2a",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "b",
                    "description": "(-b ± √(b² - 4ac))/2a",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "c",
                    "description": "(-b ± √(b² - 4ac))/2a",
                    "type": 3,
                    "required": True
                }
            ]
        },
        {
            "name": "rpn",
            "description": "Reverse Polish Notation",
            "type": 1,
            "options": [
                {
                    "name": "equation",
                    "description": "The equation to solve",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "radians",
                    "description": "Whether or not to use radians. Degrees by default",
                    "type": 5,
                    "required": False
                }
            ]
        },
        {
            "name": "substitute",
            "description": "Substitute a value into an equation",
            "type": 1,
            "options": [
                {
                    "name": "variable",
                    "description": "Name of the variable, eg x, y, z",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "value",
                    "description": "Value for the variable",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "equation",
                    "description": "The equation to solve",
                    "type": 3,
                    "required": True
                },
                {
                    "name": "radians",
                    "description": "Whether or not to use radians. Degrees by default",
                    "type": 5,
                    "required": False
                }
            ]
        },
        {
            "name": "factorial",
            "description": "Find the factorial of a number",
            "type": 1,
            "options": [
                {
                    "name": "number",
                    "description": "The number to find the factorial of",
                    "type": 4,
                    "required": True
                }
            ]
        },
        {
            "name": "triangle",
            "description": "Triangle solver",
            "type": 1,
            "options": [
                {
                    "name": "a",
                    "description": "Value for angle A. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "b",
                    "description": "Value for angle B. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "c",
                    "description": "Value for angle C. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "x",
                    "description": "Value for side X. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "y",
                    "description": "Value for side Y. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "z",
                    "description": "Value for side Z. This is a shortcut",
                    "type": 3,
                    "required": False
                },
                {
                    "name": "radians",
                    "description": "Whether or not to use radians. This is a shortcut",
                    "type": 5,
                    "required": False
                },
                {
                    "name": "now",
                    "description": "Whether or not to solve now. Normally will bring up the editor",
                    "type": 5,
                    "required": False
                }
            ]
        },
        {
            "name": "factor",
            "description": "List all factors of a given number",
            "type": 1,
            "options": [
                {
                    "name": "number",
                    "description": "The number to find the factors of",
                    "type": 4,
                    "required": True
                }
            ]
        },
        {
            "name": "radical",
            "description": "Reduces a radical, eg √8 = 2√2",
            "type": 1,
            "options": [
                {
                    "name": "x",
                    "description": "x in ˣ√y",
                    "type": 4,
                    "required": True
                },
                {
                    "name": "y",
                    "description": "y in ˣ√y",
                    "type": 4,
                    "required": True
                }
            ]
        }
    }
}
