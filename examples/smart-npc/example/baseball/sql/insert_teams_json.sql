delete from smartnpc.teams;

INSERT INTO smartnpc.teams(
    team_id,
    team_name,
    team_year,
    description,
    roster,
    default_lineup
)
VALUES (
    'Red',
    'Red',
    2025,
    'Known for their aggressive batting style and powerful offense. Hailing from the sunny shores, the Coastal Comets bring a dynamic blend of speed and power to the diamond.',
    '{
  "pitchers":[{
    "name": "Michael Nguyen",
    "stats": {
      "this_season": {
        "GP": 16,
        "GS": 15,
        "CG": 3,
        "SHO": 3,
        "IP": 77.6,
        "H": 99,
        "R": 36,
        "ER": 31,
        "HR": 4,
        "BB": 44,
        "K": 91
      },
      "career": {
        "GP": 176,
        "GS": 150,
        "CG": 9,
        "SHO": 12,
        "IP": 771.7,
        "H": 1062,
        "R": 361,
        "ER": 310,
        "HR": 34,
        "BB": 521,
        "K": 874
      }
    }
  }],
  "fielders": [
    {
      "position": "CF",
      "name": "Ryuichi Suzuki",
      "hand": "Left",
      "avg": 0.315,
      "hr": 9,
      "rbi": 51,
      "notes": "High average, contact hitter, limited power."
    },
    {
      "position": "2B",
      "name": "Robert Ackley",
      "hand": "Left",
      "avg": 0.226,
      "hr": 12,
      "rbi": 50,
      "notes": "Some power, but struggled with consistency."
    },
    {
      "position": "C",
      "name": "Jon Montero",
      "hand": "Left",
      "avg": 0.26,
      "hr": 15,
      "rbi": 62,
      "notes": "Developing power hitter, still inconsistent."
    },
    {
      "position": "1B",
      "name": "Mark Smoak",
      "hand": "Both",
      "avg": 0.217,
      "hr": 19,
      "rbi": 51,
      "notes": "Switch-hitter, power potential, low average."
    },
    {
      "position": "DH",
      "name": "Joel Carp",
      "hand": "Left",
      "avg": 0.213,
      "hr": 5,
      "rbi": 18,
      "notes": "Limited at-bats, low batting average."
    },
    {
      "position": "3B",
      "name": "Richard Seager",
      "hand": "Left",
      "avg": 0.259,
      "hr": 20,
      "rbi": 86,
      "notes": "Good power for a middle infielder."
    },
    {
      "position": "RF",
      "name": "Brett Saunders",
      "hand": "Left",
      "avg": 0.247,
      "hr": 19,
      "rbi": 57,
      "notes": "Power and speed, high strikeout rate."
    },
    {
      "position": "LF",
      "name": "Paul Wells",
      "hand": "Right",
      "avg": 0.228,
      "hr": 10,
      "rbi": 36,
      "notes": "Power potential, but inconsistent contact overall."
    },
    {
      "position": "SS",
      "name": "James Ryan",
      "hand": "Right",
      "avg": 0.194,
      "hr": 3,
      "rbi": 31,
      "notes": "Very weak hitter, almost no power."
    }
  ]
}',
    '{
  "pitcher": {
    "name": "Michael Nguyen",
    "stats": {
      "this_season": {
        "GP": 16,
        "GS": 15,
        "CG": 3,
        "SHO": 3,
        "IP": 77.6,
        "H": 99,
        "R": 36,
        "ER": 31,
        "HR": 4,
        "BB": 44,
        "K": 91
      },
      "career": {
        "GP": 176,
        "GS": 150,
        "CG": 9,
        "SHO": 12,
        "IP": 771.7,
        "H": 1062,
        "R": 361,
        "ER": 310,
        "HR": 34,
        "BB": 521,
        "K": 874
      }
    }
  },
  "fielders": [
    {
      "position": "CF",
      "name": "Ryuichi Suzuki",
      "hand": "Left",
      "avg": 0.315,
      "hr": 9,
      "rbi": 51,
      "notes": "High average, contact hitter, limited power."
    },
    {
      "position": "2B",
      "name": "Robert Ackley",
      "hand": "Left",
      "avg": 0.226,
      "hr": 12,
      "rbi": 50,
      "notes": "Some power, but struggled with consistency."
    },
    {
      "position": "C",
      "name": "Jon Montero",
      "hand": "Left",
      "avg": 0.26,
      "hr": 15,
      "rbi": 62,
      "notes": "Developing power hitter, still inconsistent."
    },
    {
      "position": "1B",
      "name": "Mark Smoak",
      "hand": "Both",
      "avg": 0.217,
      "hr": 19,
      "rbi": 51,
      "notes": "Switch-hitter, power potential, low average."
    },
    {
      "position": "DH",
      "name": "Joel Carp",
      "hand": "Left",
      "avg": 0.213,
      "hr": 5,
      "rbi": 18,
      "notes": "Limited at-bats, low batting average."
    },
    {
      "position": "3B",
      "name": "Richard Seager",
      "hand": "Left",
      "avg": 0.259,
      "hr": 20,
      "rbi": 86,
      "notes": "Good power for a middle infielder."
    },
    {
      "position": "RF",
      "name": "Brett Saunders",
      "hand": "Left",
      "avg": 0.247,
      "hr": 19,
      "rbi": 57,
      "notes": "Power and speed, high strikeout rate."
    },
    {
      "position": "LF",
      "name": "Paul Wells",
      "hand": "Right",
      "avg": 0.228,
      "hr": 10,
      "rbi": 36,
      "notes": "Power potential, but inconsistent contact overall."
    },
    {
      "position": "SS",
      "name": "James Ryan",
      "hand": "Right",
      "avg": 0.194,
      "hr": 3,
      "rbi": 31,
      "notes": "Very weak hitter, almost no power."
    }
  ]
}'
);

INSERT INTO smartnpc.teams(
    team_id,
    team_name,
    team_year,
    description,
    roster,
    default_lineup
)
VALUES (
    'Blue',
    'Blue',
    2025,
    'A team known for its strong pitching and solid defensive play. Forged in the heartland, the Ironclad Armadillos are a team built on grit and resilience.',
    '{
  "pitchers": [{
    "name": "Hank Wilder",
    "stats": {
      "this_season": {
        "GP": 16,
        "GS": 15,
        "CG": 3,
        "SHO": 3,
        "IP": 77.6,
        "H": 99,
        "R": 36,
        "ER": 31,
        "HR": 4,
        "BB": 44,
        "K": 91
      },
      "career": {
        "GP": 176,
        "GS": 150,
        "CG": 9,
        "SHO": 12,
        "IP": 771.7,
        "H": 1062,
        "R": 361,
        "ER": 310,
        "HR": 34,
        "BB": 521,
        "K": 874
      }
    }
  }],
  "fielders": [
    {
      "position": "CF",
      "name": "Grant Trout",
      "hand": "Right",
      "avg": 0.326,
      "hr": 30,
      "rbi": 83,
      "notes": "Exceptional rookie, speed and power combo."
    },
    {
      "position": "SS",
      "name": "Aris Aybar",
      "hand": "Both",
      "avg": 0.29,
      "hr": 8,
      "rbi": 45,
      "notes": "Switch-hitter, good contact, solid average."
    },
    {
      "position": "1B",
      "name": "Sandeep Pujols",
      "hand": "Right",
      "avg": 0.285,
      "hr": 30,
      "rbi": 105,
      "notes": "Still potent, but declining from peak."
    },
    {
      "position": "RF",
      "name": "Jaime Hunter",
      "hand": "Right",
      "avg": 0.313,
      "hr": 16,
      "rbi": 92,
      "notes": "Consistent hitter, good average and RBIs."
    },
    {
      "position": "DH",
      "name": "Francis Trumbo",
      "hand": "Right",
      "avg": 0.268,
      "hr": 32,
      "rbi": 95,
      "notes": "Big power, high strikeout, solid production."
    },
    {
      "position": "LF",
      "name": "Maurice Mathers",
      "hand": "Right",
      "avg": 0.23,
      "hr": 11,
      "rbi": 29,
      "notes": "Struggling veteran, low average, limited power."
    },
    {
      "position": "2B",
      "name": "Dre Kendrick",
      "hand": "Right",
      "avg": 0.287,
      "hr": 8,
      "rbi": 67,
      "notes": "Solid contact hitter, decent average."
    },
    {
      "position": "3B",
      "name": "Jose Callaspo",
      "hand": "Both",
      "avg": 0.252,
      "hr": 10,
      "rbi": 53,
      "notes": "Decent contact, switch-hitter, average power."
    },
    {
      "position": "C",
      "name": "Jesus Iannetta",
      "hand": "Right",
      "avg": 0.24,
      "hr": 9,
      "rbi": 26,
      "notes": "Some power, lower batting average overall."
    }
  ]
}',
    '{
  "pitcher": {
    "name": "Hank Wilder",
    "stats": {
      "this_season": {
        "GP": 16,
        "GS": 15,
        "CG": 3,
        "SHO": 3,
        "IP": 77.6,
        "H": 99,
        "R": 36,
        "ER": 31,
        "HR": 4,
        "BB": 44,
        "K": 91
      },
      "career": {
        "GP": 176,
        "GS": 150,
        "CG": 9,
        "SHO": 12,
        "IP": 771.7,
        "H": 1062,
        "R": 361,
        "ER": 310,
        "HR": 34,
        "BB": 521,
        "K": 874
      }
    }
  },
  "fielders": [
    {
      "position": "CF",
      "name": "Grant Trout",
      "hand": "Right",
      "avg": 0.326,
      "hr": 30,
      "rbi": 83,
      "notes": "Exceptional rookie, speed and power combo."
    },
    {
      "position": "SS",
      "name": "Aris Aybar",
      "hand": "Both",
      "avg": 0.29,
      "hr": 8,
      "rbi": 45,
      "notes": "Switch-hitter, good contact, solid average."
    },
    {
      "position": "1B",
      "name": "Sandeep Pujols",
      "hand": "Right",
      "avg": 0.285,
      "hr": 30,
      "rbi": 105,
      "notes": "Still potent, but declining from peak."
    },
    {
      "position": "RF",
      "name": "Jaime Hunter",
      "hand": "Right",
      "avg": 0.313,
      "hr": 16,
      "rbi": 92,
      "notes": "Consistent hitter, good average and RBIs."
    },
    {
      "position": "DH",
      "name": "Francis Trumbo",
      "hand": "Right",
      "avg": 0.268,
      "hr": 32,
      "rbi": 95,
      "notes": "Big power, high strikeout, solid production."
    },
    {
      "position": "LF",
      "name": "Maurice Mathers",
      "hand": "Right",
      "avg": 0.23,
      "hr": 11,
      "rbi": 29,
      "notes": "Struggling veteran, low average, limited power."
    },
    {
      "position": "2B",
      "name": "Dre Kendrick",
      "hand": "Right",
      "avg": 0.287,
      "hr": 8,
      "rbi": 67,
      "notes": "Solid contact hitter, decent average."
    },
    {
      "position": "3B",
      "name": "Jose Callaspo",
      "hand": "Both",
      "avg": 0.252,
      "hr": 10,
      "rbi": 53,
      "notes": "Decent contact, switch-hitter, average power."
    },
    {
      "position": "C",
      "name": "Jesus Iannetta",
      "hand": "Right",
      "avg": 0.24,
      "hr": 9,
      "rbi": 26,
      "notes": "Some power, lower batting average overall."
    }
  ]
}'
);