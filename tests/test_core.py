
import sys
import os
import pytest
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from core.controller import CoreController
from aggregation.controller import AggregationController
from edge.controller import EdgeController
from ml.threat_detector import ThreatDetector
from ml.load_balancer import LoadBalancer

# CoreController tests
def test_core_controller_init():
    c = CoreController()
    assert isinstance(c.app, Flask)
    assert hasattr(c, 'aggregation_controllers')

def test_core_controller_health():
    c = CoreController()
    client = c.app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'

# AggregationController tests
def test_aggregation_controller_init():
    a = AggregationController('http://localhost:5000')
    assert isinstance(a.app, Flask)
    assert hasattr(a, 'edge_controllers')

def test_aggregation_controller_health():
    a = AggregationController('http://localhost:5000')
    client = a.app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'

# EdgeController tests
def test_edge_controller_init():
    e = EdgeController('http://localhost:5001')
    assert isinstance(e.app, Flask)

def test_edge_controller_health():
    e = EdgeController('http://localhost:5001')
    client = e.app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.json['status'] == 'ok'

# ThreatDetector tests
def test_threat_detector():
    td = ThreatDetector()
    X = [[10, 100], [20, 200], [30, 300]]
    td.train(X)
    result = td.detect({'packets': 10, 'bytes': 100})
    assert 'threat' in result

# LoadBalancer tests
def test_load_balancer():
    lb = LoadBalancer(['http://localhost:5001', 'http://localhost:5002'])
    # Mock get_controller_load to avoid real HTTP calls
    lb.get_controller_load = lambda url: 1 if url.endswith('5001') else 2
    best = lb.balance({'packets': 1, 'bytes': 1})
    assert best == 'http://localhost:5001'
