## Quickstarts for Spanner

This directory contains quickstarts that allow you to deploy Cloud Spanner tables for games. It assumes you have a Cloud Spanner instance and a dataset in the correct region. 

For really simple setup, you can just create Players table and GameTelemetry tables. The other tables provide more capacities, like leaderboard, in-game-purchase. 

Cloud Spanner provides good scalability. As long as good key is designed, the same set of tables can scale automatically to handle fair large game, with significant QPS and throughput. Perhaps some second-indexes can be created to enhance performance. 

A short data insert script is also included for demo purpose only. 
