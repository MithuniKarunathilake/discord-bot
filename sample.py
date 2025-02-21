from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)