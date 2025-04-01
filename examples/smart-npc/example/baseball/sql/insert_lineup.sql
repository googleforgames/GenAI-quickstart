delete from smartnpc.lineup;
INSERT INTO smartnpc.lineup(
    team_id,
    player_id,
    session_id,
    lineup
)
VALUES (
    '1927-New-York-Yankees',
    'JackBuser',
    'random_session2',
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

INSERT INTO smartnpc.lineup(
    team_id,
    player_id,
    session_id,
    lineup
)
VALUES (
    '1969-New-York-Mets',
    'Computer',
    'random_session2',
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

