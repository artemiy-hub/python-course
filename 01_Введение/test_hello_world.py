import subprocess

def test_hello_world():
    result = subprocess.run(["python", "hello_world.py"], capture_output=True, text=True)
    assert result.stdout.strip() == "Привет, мир!" 