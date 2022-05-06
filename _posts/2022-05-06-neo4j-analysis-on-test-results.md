---
layout: post
title: Neo4J analysis on Test Results
date: 2022-05-06 10:20 +0000
categories: [Tips & Tricks]
tags: [neo4j]
comments: false
excerpt: Analise your test results data using a graph database
---

## Use Case
Test results executed in a Jenkins job or from local machine can be stored and analised using a graph based database as Neo4j.
**Why:** because is much easier and intuitive to represent data usign graphs.

[Neo4j](https://neo4j.com/) is a [Graph Database](https://en.wikipedia.org/wiki/Graph_database) wich help us to visualize and analyze data using its own query language called [Cypher](https://neo4j.com/developer/cypher/)

## Start Neo4J
I am using here [docker-compose](https://docs.docker.com/compose/) to spin up easily a desired version.

As you can see bellow, I'm adding volume shares from host to guest container.
* in data I save the Jenkins results (xml) - that ca be parsed and normilized to be sent to Neo4J
* in logs - I save DB logs

```ruby
# docker-compose.yml
version: '2'
services:    
  neo4j:  
    image: neo4j:3.5
    volumes: 
      - ./data:/data
      - ./data/logs:/logs
    ports:
      - 7474:7474
      - 7687:7687
    environment:
      - NEO4J_AUTH=neo4j/admin
      - NEO4JLABS_PLUGINS='["graph-data-science"]'
```

## Graph Database for Test Case Analysis
> this is the graph database "schema" that we can use to analyze the Test Case executed on a particular build

![neo4j](/images/posts/neo4j-tests.png)


## Cypher Queries
> read more [here](https://neo4j.com/developer/cypher/) about Cypher

```cypher
// cleanup
MATCH (n) DETACH DELETE n

// how many tags not related to B- 
MATCH (t:Tag) where not(t.name contains "B-")  RETURN t.name
```

* duration

```cypher
//what are the top 20 slowest test suites 
MATCH (p:Project)-[]->(b:Build)-[e]->(ts:TestSuite) WHERE p.name="projecA-238"  RETURN distinct(ts.name), b.name, e.duration/60 as durationInMinutes ORDER BY durationInMinutes DESC LIMIT 20

// what are the top 20 slowest tests
MATCH (p:Project)-[]->(b:Build)-[e]->(ts:TestSuite)-[r]->(tc:TestCase) WHERE p.name="projecA-238"  RETURN distinct(tc.name), b.name, r.duration/60 as durationInMinutes ORDER BY durationInMinutes DESC LIMIT 20

// How much time do we spent on teardown
MATCH (teardown:Teardown)-[clean]->(testSuite:TestSuite)<-[]-(build:Build)<-[]-(project:Project) WHERE project.name='projecA-238' MATCH (teardown)-[]->(library:Library) RETURN distinct(teardown.name) as teardownName, count(*) as usage , sum(clean.duration/60) as durationMin, library.name ORDER BY usage DESC

// How much time do we spent on precondition
MATCH (setup:Setup)-[sr]->(testSuite:TestSuite)<-[]-(build:Build)<-[]-(project:Project) WHERE project.name='projecA-238' RETURN distinct(setup.name), count(setup) as usage, sum(sr.duration) ORDER BY usage DESC

MATCH (setup:Setup)-[sr]->(testSuite:TestSuite)<-[]-(build:Build)<-[]-(project:Project) WHERE project.name='projecA-238' MATCH (setup)-[]->(library:Library) RETURN distinct(setup.name), count(setup) as usage, sum(sr.duration/60) as durationMin, library.name ORDER BY usage DESC
```

* Pass/Fail

```cypher
//how many setup conditions failed per stories
MATCH (project:Project)-[]->(b:Build)-[r]->(ts:TestSuite)<-[s:PREPARE]-(setup:Setup) WHERE project.name="projecA-238" and s.status="FAIL" MATCH (ts)-[]->(t:TestCase) return ts.name, setup.name, s.duration/60 as setupDuration, s.status, count(t) as FailedTestCase order by FailedTestCase DESC

// test cases failed per suite
MATCH (testSuite:TestSuite)-[ex]->(testCase:TestCase) where ex.status="FAIL" return testSuite.name, count(testCase) as testCaseFailed  order by testCaseFailed DESC
```


* count

```cypher
//how many calls are made to a particular test step

MATCH (n:TestStep)<-[s:STEP_OF]-(f) return distinct(n.name), count(s) as uni order by uni desc limit 20
```