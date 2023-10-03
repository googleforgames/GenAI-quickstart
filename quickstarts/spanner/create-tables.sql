--table for players. The attributes field is a byte stream of serialized structure data.  
CREATE TABLE Players (
  playerUUID STRING(36) NOT NULL,
  player_name STRING(MAX) NOT NULL,
  email STRING(MAX) NOT NULL,
  password_hash BYTES(60) NOT NULL,
  created TIMESTAMP,
  updated TIMESTAMP,
  stats JSON,
  account_balance NUMERIC NOT NULL DEFAULT (0.00),
  is_logged_in BOOL,
  last_login TIMESTAMP,
  valid_email BOOL,
  attributes BYTES(MAX),
  purchased_items BYTES(MAX),
) PRIMARY KEY(playerUUID);

--table for game telemetry. This is good for a simple game. 
CREATE TABLE GameTelemetry (
  eventId STRING(1024) NOT NULL,
  playerUUID STRING(36),
  username STRING(1024),
  datetime STRING(1024),
  numberSessions INT64,
  points FLOAT64,
  totalTransactionAmount FLOAT64,
  itemsPurchased INT64,
  visitsToStore INT64,
  minutesPlayed FLOAT64,
  gameType STRING(1024),
  newFriends INT64,
  offensePercentage FLOAT64,
  defensePercentage FLOAT64,
  timeWithBall FLOAT64,
  platform STRING(1024),
  FOREIGN KEY(playerUUID) REFERENCES Players(playerUUID),
) PRIMARY KEY(eventId);


--table for game sessions, with players and winners recorded. 
CREATE TABLE Sessions (
  sessionUUID STRING(36) NOT NULL,
  players ARRAY<STRING(36)>,
  winner STRING(36),
  created TIMESTAMP,
  finished TIMESTAMP,
) PRIMARY KEY(sessionUUID);

--table for leader board
CREATE TABLE SessionRanking (
  sessionUUID STRING(36) NOT NULL,
  playerUUID STRING(36) NOT NULL,
  score INT64,  
  FOREIGN KEY(playerUUID) REFERENCES Players(playerUUID),
  FOREIGN KEY(sessionUUID) REFERENCES Sessions(sessionUUID),
) PRIMARY KEY(sessionUUID, playerUUID);

CREATE INDEX idx_score_ranking ON SessionRanking (
        sessionUUID,
        score DESC
);


--table for in-app-purchase. purchase details are in byte stream 
CREATE TABLE InAppPurchase (
   playerUUID STRING(36) NOT NULL,
   sessionUUID STRING(36) NOT NULL,
   purchaseUUID STRING(36) NOT NULL,
   purchase_total_price FLOAT64,
   created TIMESTAMP,
   purchaseLog BYTES(MAX),
  FOREIGN KEY(playerUUID) REFERENCES Players(playerUUID),
  FOREIGN KEY(sessionUUID) REFERENCES Sessions(sessionUUID),
)PRIMARY KEY(playerUUID, sessionUUID, purchaseUUID),
 INTERLEAVE IN PARENT Players ON DELETE CASCADE;

--table for inventory
CREATE TABLE ItemInventory (
  item_id STRING(MAX) NOT NULL,
  item_name STRING(MAX),
  item_keyword STRING(MAX),
  item_description STRING(MAX),
  item_info BYTES(MAX),
  item_category STRING(MAX),
  item_price NUMERIC,
  active_since DATE,
  is_active BOOL,
  is_instock BOOL,
  is_new BOOL,
  is_bestseller BOOL,
) PRIMARY KEY(item_id);
