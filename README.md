# IOT-EDGE


![Description](images/1.png)


# Installation

Clone this repository:
~~~~
git clone https://github.com/af-mm/IOT-EDGE.git
~~~~

Create data directories:
~~~~
./createDataDirs.sh
~~~~

Build docker images:
~~~~
docker-compose build
~~~~

Run docker-compose:
~~~~
./run.sh
~~~~

Create Kafka topics:
~~~~
./createTopics.sh
~~~~

Done!


# Running

Parameters are places in ".env" file. Change them if it is needed.
Then, run:

~~~~
./run.sh
~~~~
