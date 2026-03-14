// __tests__/yaml-parser.test.js
import { parseFrontmatter, parseVersionRequirement } from '../lib/core/yaml-parser.js';

describe('yaml-parser', () => {
  describe('parseFrontmatter', () => {
    test('extracts valid YAML frontmatter', () => {
      const content = `---
name: test-skill
version: 1.0.0
tdd_first: true
---
# Hello`;

      const result = parseFrontmatter(content);
      expect(result).toEqual({
        name: 'test-skill',
        version: '1.0.0',
        tdd_first: true,
      });
    });

    test('returns null when no frontmatter', () => {
      const content = `# Just a heading
No YAML here.`;
      expect(parseFrontmatter(content)).toBeNull();
    });

    test('handles empty frontmatter', () => {
      const content = `---
---
# Hello`;
      expect(parseFrontmatter(content)).toBeNull();
    });

    test('handles multiline frontmatter', () => {
      const content = `---
requirements:
  unity_version: ">=6.0"
  render_pipeline: "URP"
  dependencies:
    - "com.unity.burst"
    - "com.unity.inputsystem"
---
# Content`;

      const result = parseFrontmatter(content);
      expect(result.requirements.unity_version).toBe('>=6.0');
      expect(result.requirements.dependencies).toContain('com.unity.burst');
    });

    test('handles Windows line endings (CRLF)', () => {
      const content = '---\r\nname: test\r\n---\r\n';
      const result = parseFrontmatter(content);
      expect(result.name).toBe('test');
    });
  });

  describe('parseVersionRequirement', () => {
    test('parses >=6.0', () => {
      expect(parseVersionRequirement('>=6.0')).toBe(6);
    });

    test('parses >=2022.3', () => {
      expect(parseVersionRequirement('>=2022.3')).toBe(2022);
    });

    test('handles empty string', () => {
      expect(parseVersionRequirement('')).toBe(0);
    });

    test('handles null/undefined', () => {
      expect(parseVersionRequirement(null)).toBe(0);
      expect(parseVersionRequirement(undefined)).toBe(0);
    });

    test('handles no number in string', () => {
      expect(parseVersionRequirement('latest')).toBe(0);
    });
  });
});
