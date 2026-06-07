const markdownlint = require("markdownlint");

module.exports = {
  "names": [ "obsidian-title-enforcement" ],
  "description": "Enforce Obsidian-style frontmatter titles in docs/, forbid elsewhere.",
  "tags": [ "frontmatter", "title" ],
  "function": function rule(params, onError) {
    const file = params.name;
    const isDocs = file.split(/[\\/]/).includes("docs");
    const frontMatterTitle = params.frontMatterLines.length > 0;

    // MD041 logic is partially handled here to enforce context-specific behavior,
    // But mainly we want to check if frontMatter is allowed/required.

    if (isDocs) {
      // Requirement: "should have a YAML-frontmatter"
      if (!frontMatterTitle) {
        // Double-check if it has a generic frontmatter but no title?
        // User said "have a YAML-frontmatter (Obsidian-style)". Usually means 'title: ...'
        // But for now, let's just check if ANY frontmatter lines exist.
        // params.frontMatterLines is the array of lines.
        onError({
            lineNumber: 1,
            detail: "Files in 'docs' directories must have YAML frontmatter.",
            context: "Missing frontmatter"
        });
      }
    } else {
      // Requirement: "should not have a YAML-frontmatter"
      if (frontMatterTitle) {
        onError({
            lineNumber: 1,
            detail: "Files outside 'docs' directories should not have YAML frontmatter.",
            context: "Unexpected frontmatter"
        });
      }
    }
  }
};
