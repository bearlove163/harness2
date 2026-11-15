import os
import json
import ast
import nbformat

def test_json_configs():
    config_path = os.path.join("configs", "architectural_video_prompts.json")
    assert os.path.exists(config_path), "Config file does not exist"
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "categories" in data
    assert "upstream_relay_rules" in data
    categories = data["categories"]
    required_cats = ["massing_and_exterior", "structural_systems", "tectonic_details", "humanities_and_history"]
    for cat in required_cats:
        assert cat in categories, f"Missing category: {cat}"
        presets = categories[cat]["presets"]
        assert len(presets) > 0, f"No presets in category: {cat}"
        for p in presets:
            assert "prompt_zh" in p
            assert "prompt_en" in p
            assert "recommended_camera" in p
    print(f"✅ [Test 1 Passed] configs/architectural_video_prompts.json verified ({len(categories)} categories, {sum(len(c['presets']) for c in categories.values())} presets)")

def test_notebook_structure_and_syntax():
    nb_path = os.path.join("notebooks", "Wan2_1_Architecture_Video_Colab.ipynb")
    assert os.path.exists(nb_path), "Notebook does not exist"
    
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
    
    assert len(nb.cells) >= 7, f"Expected at least 7 cells, got {len(nb.cells)}"
    
    # Check all code cells for syntax validity (excluding colab magic ! lines)
    code_cells = [c for c in nb.cells if c.cell_type == "code"]
    for idx, cell in enumerate(code_cells, 1):
        clean_lines = []
        for line in cell.source.splitlines():
            # strip colab bash magic lines for python AST parse check
            if line.strip().startswith("!") or line.strip().startswith("%"):
                clean_lines.append("# " + line)
            else:
                clean_lines.append(line)
        cleaned_source = "\n".join(clean_lines)
        try:
            ast.parse(cleaned_source)
        except SyntaxError as e:
            raise AssertionError(f"Syntax error in code cell {idx}: {e}")
            
    print(f"✅ [Test 2 Passed] notebooks/Wan2_1_Architecture_Video_Colab.ipynb verified ({len(nb.cells)} cells, all code valid AST)")

def test_requirements_file():
    req_path = "requirements-colab.txt"
    assert os.path.exists(req_path), "requirements-colab.txt missing"
    with open(req_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    assert len(lines) >= 8, f"Expected dependencies, got {len(lines)}"
    print(f"✅ [Test 3 Passed] requirements-colab.txt verified ({len(lines)} dependencies)")

if __name__ == "__main__":
    test_json_configs()
    test_notebook_structure_and_syntax()
    test_requirements_file()
    print("🎉 All verification tests passed successfully!")
