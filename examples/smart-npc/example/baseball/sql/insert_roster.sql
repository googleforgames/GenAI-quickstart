delete from smartnpc.rosters;
INSERT INTO smartnpc.rosters(
    team_id,
    session_id,
    player_id,
    roster
)
VALUES (
    '1927-New-York-Yankees',
    'random_session2',
    'JackBuser',
    '
{
  "pitchers": [
    {
      "name": "Thomas Anderson",
      "stats": {
        "this_season": {
          "GP": 20,
          "GS": 20,
          "CG": 1,
          "SHO": 1,
          "IP": 104.0,
          "H": 65,
          "R": 38,
          "ER": 36,
          "HR": 6,
          "BB": 44,
          "K": 145
        },
        "career": {
          "GP": 211,
          "GS": 211,
          "CG": 1,
          "SHO": 1,
          "IP": 1096.2,
          "H": 840,
          "R": 419,
          "ER": 389,
          "HR": 108,
          "BB": 495,
          "K": 1368
        }
      }
    },
    {
      "name": "David Brown",
      "stats": {
        "this_season": {
          "GP": 18,
          "GS": 18,
          "CG": 0,
          "SHO": 0,
          "IP": 92.0,
          "H": 72,
          "R": 42,
          "ER": 40,
          "HR": 8,
          "BB": 32,
          "K": 120
        },
        "career": {
          "GP": 185,
          "GS": 185,
          "CG": 2,
          "SHO": 2,
          "IP": 950.1,
          "H": 750,
          "R": 380,
          "ER": 350,
          "HR": 95,
          "BB": 400,
          "K": 1100
        }
      }
    },
     {
      "name": "Maria Garcia",
      "stats": {
        "this_season": {
          "GP": 22,
          "GS": 22,
          "CG": 2,
          "SHO": 1,
          "IP": 120.0,
          "H": 80,
          "R": 35,
          "ER": 32,
          "HR": 5,
          "BB": 28,
          "K": 160
        },
        "career": {
          "GP": 200,
          "GS": 200,
          "CG": 10,
           "SHO": 5,
          "IP": 1100.0,
          "H": 700,
          "R": 300,
          "ER": 275,
          "HR": 75,
          "BB": 350,
          "K": 1250
        }
      }
    },
    {
      "name": "Michael Johnson",
      "stats": {
        "this_season": {
          "GP": 15,
          "GS": 15,
          "CG": 0,
          "SHO": 0,
          "IP": 78.0,
          "H": 60,
          "R": 30,
          "ER": 28,
          "HR": 7,
          "BB": 25,
          "K": 100
        },
        "career": {
          "GP": 160,
          "GS": 160,
          "CG": 5,
          "SHO": 3,
          "IP": 850.0,
          "H": 650,
          "R": 320,
          "ER": 300,
          "HR": 80,
          "BB": 380,
          "K": 1050
        }
      }
    },
    {
      "name": "Jessica Lee",
       "stats": {
        "this_season": {
          "GP": 19,
          "GS": 19,
          "CG": 1,
          "SHO": 1,
          "IP": 98.0,
          "H": 70,
          "R": 32,
          "ER": 30,
          "HR": 4,
          "BB": 35,
          "K": 130
        },
        "career": {
          "GP": 195,
          "GS": 195,
          "CG": 8,
          "SHO": 4,
          "IP": 1000.0,
          "H": 780,
          "R": 350,
          "ER": 320,
          "HR": 90,
          "BB": 420,
          "K": 1200
        }
      }
    },
     {
      "name": "Kevin Rodriguez",
      "stats": {
         "this_season": {
          "GP": 21,
          "GS": 21,
          "CG": 0,
          "SHO": 0,
          "IP": 110.0,
          "H": 85,
          "R": 45,
          "ER": 42,
          "HR": 9,
          "BB": 40,
          "K": 150
        },
        "career": {
           "GP": 220,
          "GS": 220,
          "CG": 3,
          "SHO": 1,
          "IP": 1150.0,
          "H": 900,
          "R": 450,
          "ER": 420,
          "HR": 110,
          "BB": 500,
          "K": 1400
        }
      }
    },
    {
      "name": "Ashley Wilson",
      "stats": {
         "this_season": {
          "GP": 17,
          "GS": 17,
          "CG": 2,
          "SHO": 2,
          "IP": 90.0,
          "H": 60,
          "R": 25,
          "ER": 22,
          "HR": 3,
          "BB": 20,
          "K": 110
        },
        "career": {
          "GP": 175,
          "GS": 175,
          "CG": 12,
          "SHO": 7,
          "IP": 900.0,
          "H": 680,
          "R": 280,
          "ER": 250,
          "HR": 70,
          "BB": 300,
          "K": 1150
        }
      }
    }
  ],
  "fielders": [
    {
      "position": "C",
      "name": "Jake Miller",
      "hand": "R",
      "avg": 0.275,
      "hr": 15,
      "rbi": 75,
      "notes": "Solid defense, decent bat."
    },
    {
      "position": "1B",
      "name": "Emily Davis",
      "hand": "L",
      "avg": 0.305,
      "hr": 22,
      "rbi": 90,
      "notes": "Power hitter, average defense."
    },
    {
      "position": "2B",
      "name": "Carlos Sanchez",
      "hand": "R",
      "avg": 0.28,
      "hr": 10,
      "rbi": 55,
      "notes": "Good contact hitter, speedy."
    },
    {
      "position": "SS",
      "name": "Sarah Jones",
      "hand": "L",
      "avg": 0.26,
      "hr": 5,
      "rbi": 40,
       "notes": "Excellent fielder, good on-base percentage."
    },
    {
      "position": "3B",
      "name": "Brandon Lee",
      "hand": "R",
      "avg": 0.295,
      "hr": 18,
      "rbi": 80,
       "notes": "Consistent hitter, good arm."
    },
    {
      "position": "LF",
      "name": "Megan Green",
      "hand": "L",
      "avg": 0.27,
      "hr": 12,
      "rbi": 65,
       "notes": "Good range, average hitter."
    },
    {
      "position": "CF",
      "name": "Tyler Wilson",
      "hand": "R",
      "avg": 0.315,
      "hr": 8,
      "rbi": 50,
       "notes":"Leadoff hitter, good speed."
    },
    {
      "position": "RF",
      "name": "Kayla Martinez",
      "hand": "L",
      "avg": 0.29,
      "hr": 16,
      "rbi": 70,
       "notes": "Strong arm, good power."
    },
    {
      "position": "DH",
      "name": "Christopher Garcia",
      "hand": "R",
      "avg": 0.285,
      "hr": 20,
      "rbi": 85,
       "notes": "Power hitter, clutch performer."
    }
  ]
}
    '
);

INSERT INTO smartnpc.rosters(
    team_id,
    session_id,
    player_id,
    roster
)
VALUES (
    '1969-New-York-Mets',
    'random_session2',
    'Computer',
    '
{
  "pitchers": [
    {
      "name": "Maria Garcia",
      "stats": {
        "this_season": {
          "GP": 18,
          "GS": 17,
          "CG": 2,
          "SHO": 1,
          "IP": 98.2,
          "H": 72,
          "R": 35,
          "ER": 32,
          "HR": 8,
          "BB": 28,
          "K": 132
        },
        "career": {
          "GP": 192,
          "GS": 185,
          "CG": 9,
          "SHO": 6,
          "IP": 1050.1,
          "H": 785,
          "R": 395,
          "ER": 360,
          "HR": 92,
          "BB": 410,
          "K": 1280
        }
      }
    },
    {
      "name": "David Lee",
      "stats": {
        "this_season": {
          "GP": 22,
          "GS": 22,
          "CG": 0,
          "SHO": 0,
          "IP": 118.0,
          "H": 85,
          "R": 48,
          "ER": 45,
          "HR": 11,
          "BB": 35,
          "K": 155
        },
        "career": {
          "GP": 208,
          "GS": 205,
          "CG": 3,
          "SHO": 2,
          "IP": 1125.3,
          "H": 810,
          "R": 430,
          "ER": 405,
          "HR": 105,
          "BB": 465,
          "K": 1390
        }
      }
    },
    {
      "name": "Jessica Brown",
      "stats": {
        "this_season": {
          "GP": 15,
          "GS": 14,
          "CG": 1,
          "SHO": 0,
          "IP": 82.1,
          "H": 62,
          "R": 28,
          "ER": 25,
          "HR": 5,
          "BB": 22,
          "K": 115
        },
        "career": {
          "GP": 165,
          "GS": 158,
          "CG": 6,
          "SHO": 3,
          "IP": 890.2,
          "H": 705,
          "R": 315,
          "ER": 290,
          "HR": 78,
          "BB": 350,
          "K": 1210
        }
      }
    },
    {
      "name": "Michael Wilson",
      "stats": {
        "this_season": {
          "GP": 19,
          "GS": 19,
          "CG": 2,
          "SHO": 1,
          "IP": 105.2,
          "H": 78,
          "R": 32,
          "ER": 29,
          "HR": 7,
          "BB": 30,
          "K": 140
        },
        "career": {
          "GP": 182,
          "GS": 178,
          "CG": 8,
          "SHO": 5,
          "IP": 960.0,
          "H": 750,
          "R": 360,
          "ER": 335,
          "HR": 85,
          "BB": 420,
          "K": 1250
        }
      }
    },
    {
      "name": "Ashley Rodriguez",
       "stats": {
        "this_season": {
          "GP": 21,
          "GS": 20,
          "CG": 0,
          "SHO": 0,
          "IP": 112.0,
          "H": 90,
          "R": 52,
          "ER": 49,
          "HR": 12,
          "BB": 40,
          "K": 160
        },
        "career": {
          "GP": 202,
          "GS": 198,
          "CG": 4,
          "SHO": 2,
          "IP": 1080.1,
          "H": 820,
          "R": 450,
          "ER": 425,
           "HR": 115,
          "BB": 480,
          "K": 1420
        }
      }
    },
    {
      "name": "Kevin Martinez",
       "stats": {
         "this_season": {
          "GP": 16,
          "GS": 15,
          "CG": 1,
          "SHO": 1,
          "IP": 88.1,
          "H": 68,
          "R": 25,
          "ER": 22,
          "HR": 4,
          "BB": 25,
          "K": 120
        },
        "career": {
          "GP": 175,
          "GS": 170,
          "CG": 7,
          "SHO": 5,
          "IP": 940.3,
          "H": 760,
          "R": 330,
          "ER": 305,
          "HR": 75,
          "BB": 380,
          "K": 1300
        }
      }
    },
    {
      "name": "Sarah Anderson",
      "stats": {
        "this_season": {
          "GP": 23,
          "GS": 23,
          "CG": 3,
          "SHO": 2,
          "IP": 125.0,
          "H": 82,
          "R": 30,
          "ER": 27,
          "HR": 6,
          "BB": 20,
          "K": 170
        },
         "career": {
          "GP": 215,
          "GS": 210,
          "CG": 11,
          "SHO": 8,
          "IP": 1150.2,
          "H": 790,
          "R": 350,
          "ER": 320,
          "HR": 80,
          "BB": 390,
          "K": 1450
        }
      }
    }
  ],
   "fielders": [
    {
      "position": "C",
      "name": "Samuel Rivera",
      "hand": "R",
      "avg": 0.260,
      "hr": 12,
      "rbi": 60,
      "notes": "Good defensive catcher, improving bat."
    },
    {
      "position": "1B",
      "name": "Olivia Chen",
      "hand": "L",
      "avg": 0.320,
      "hr": 25,
      "rbi": 100,
      "notes": "Power hitter, solid defender."
    },
    {
      "position": "2B",
      "name": "Daniel Kim",
      "hand": "R",
      "avg": 0.290,
      "hr": 8,
      "rbi": 50,
      "notes": "Excellent fielder, consistent hitter."
    },
    {
      "position": "SS",
      "name": "Sophia Rodriguez",
      "hand": "R",
      "avg": 0.275,
      "hr": 10,
      "rbi": 55,
       "notes": "Good range, strong arm at short."
    },
    {
      "position": "3B",
      "name": "Ethan Brown",
      "hand": "L",
      "avg": 0.300,
      "hr": 20,
      "rbi": 90,
      "notes": "Power hitter, clutch performer."
    },
    {
      "position": "LF",
      "name": "Ava Davis",
      "hand": "L",
      "avg": 0.280,
      "hr": 14,
      "rbi": 70,
      "notes": "Speedy outfielder, good on-base percentage."
    },
    {
      "position": "CF",
      "name": "Noah Wilson",
      "hand": "R",
      "avg": 0.310,
      "hr": 7,
      "rbi": 45,
       "notes": "Leadoff hitter, great speed."
    },
    {
      "position": "RF",
      "name": "Isabella Garcia",
      "hand": "R",
      "avg": 0.295,
      "hr": 17,
      "rbi": 80,
       "notes": "Strong arm, consistent power threat."
    },
     {
      "position": "DH",
      "name": "Jackson Smith",
      "hand": "L",
      "avg": 0.285,
      "hr": 22,
      "rbi": 95,
       "notes": "Designated hitter, pure power hitter."
    }
  ]
}
    '
);

