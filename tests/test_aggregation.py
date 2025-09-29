
import sys
import os
import pytest
from flask import Flask
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from aggregation.controller import AggregationController

def test_aggregation_controller_register(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test')
    a = AggregationController('http://localhost:5000')
    client = a.app.test_client()
    headers = {'Authorization': 'Bearer test'}
    a.edge_controllers.clear()
    resp = client.post('/register', json={'controller_type': 'edge', 'url': 'http://localhost:5002'}, headers=headers)
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'
    assert 'http://localhost:5002' in a.edge_controllers

def test_aggregation_controller_register_unauthorized():
    a = AggregationController('http://localhost:5000')
    client = a.app.test_client()
    resp = client.post('/register', json={'controller_type': 'edge', 'url': 'http://localhost:5002'})
    assert resp.status_code == 401

def test_aggregation_controller_flow_stats(monkeypatch):
    monkeypatch.setenv('SECRET_KEY', 'test')
    import requests
    monkeypatch.setattr(requests, 'post', lambda *a, **kw: type('resp', (), {'status_code': 200, 'json': lambda: {'status': 'success'}})())
    a = AggregationController('http://localhost:5000')
    client = a.app.test_client()
    headers = {'Authorization': 'Bearer test'}
    resp = client.post('/flow_stats', json={'packets': 1, 'bytes': 1}, headers=headers)
    assert resp.status_code == 200
    assert resp.json['status'] == 'success'

def test_aggregation_controller_flow_stats_unauthorized():
    a = AggregationController('http://localhost:5000')
    client = a.app.test_client()
    resp = client.post('/flow_stats', json={'packets': 1, 'bytes': 1})
    assert resp.status_code == 401
