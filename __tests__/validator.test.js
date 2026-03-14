// __tests__/validator.test.js
import { validateRequirements } from '../lib/core/validator.js';

describe('validator', () => {
  describe('validateRequirements', () => {
    const baseContext = {
      unityVersion: '6000.1.2f1',
      renderPipeline: 'URP',
      packages: ['com.unity.burst', 'com.unity.inputsystem', 'com.unity.render-pipelines.universal'],
    };

    test('passes when no requirements', () => {
      const result = validateRequirements(null, baseContext);
      expect(result.passed).toBe(true);
      expect(result.hardBlocked).toBe(false);
    });

    test('passes with empty requirements', () => {
      const result = validateRequirements({}, baseContext);
      expect(result.passed).toBe(true);
    });

    test('passes when Unity version meets requirement', () => {
      const requirements = { unity_version: '>=6.0' };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    test('fails when Unity version is too low', () => {
      const requirements = { unity_version: '>=2022.3' };
      const context = { ...baseContext, unityVersion: '2021.3.0f1' };
      const result = validateRequirements(requirements, context);
      expect(result.passed).toBe(false);
      expect(result.hardBlocked).toBe(true);
      expect(result.errors[0]).toContain('Unity version mismatch');
    });

    test('passes when render pipeline is Any', () => {
      const requirements = { render_pipeline: 'Any' };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
    });

    test('passes when render pipeline matches', () => {
      const requirements = { render_pipeline: 'URP' };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
    });

    test('fails when render pipeline does not match', () => {
      const requirements = { render_pipeline: 'HDRP' };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(false);
      expect(result.hardBlocked).toBe(true);
      expect(result.errors[0]).toContain('Render pipeline mismatch');
    });

    test('warns when package dependency is missing', () => {
      const requirements = { dependencies: ['com.unity.burst', 'com.unity.missing'] };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
      expect(result.warnings.some(w => w.includes('Missing package: com.unity.missing'))).toBe(true);
    });

    test('passes when all dependencies are present', () => {
      const requirements = { dependencies: ['com.unity.burst', 'com.unity.inputsystem'] };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
      expect(result.warnings).toHaveLength(0);
    });

    test('handles dependencies with quotes', () => {
      const requirements = { dependencies: ['"com.unity.burst"'] };
      const result = validateRequirements(requirements, baseContext);
      expect(result.passed).toBe(true);
    });
  });
});
