import test from 'node:test';
import assert from 'node:assert/strict';
import { classifyMediaJob, requireExecution } from '../examples/node/common.mjs';

test('rejects runs without explicit opt-in', () => {
  assert.throws(() => requireExecution([], { APICREST_API_KEY: 'synthetic' }), /--run/);
});
test('rejects absent or placeholder keys', () => {
  assert.throws(() => requireExecution(['--run'], {}), /APICREST_API_KEY/);
  assert.throws(() => requireExecution(['--run'], { APICREST_API_KEY: 'YOUR_API_KEY' }), /APICREST_API_KEY/);
});
test('accepts a synthetic key only after opt-in', () => {
  assert.equal(requireExecution(['--run'], { APICREST_API_KEY: 'synthetic-not-real' }), 'synthetic-not-real');
});
test('classifies documented media task states', () => {
  assert.equal(classifyMediaJob({ state: 'success', is_final: true }), 'success');
  assert.equal(classifyMediaJob({ state: 'failed', is_final: true }), 'failed');
  assert.equal(classifyMediaJob({ state: 'running', is_final: false }), 'pending');
  assert.equal(classifyMediaJob({ state: 'new-state', is_final: false }), 'unknown');
});
