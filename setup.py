from setuptools import setup, find_packages

setup(
    name="ssh_manager",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "textual",
    ],
    entry_points={
        "console_scripts": [
            "ssh_manager=ssh_manager.main:main",
        ],
    },
    package_data={
        "ssh_manager": ["*.css"],
    },
    include_package_data=True,
    author="Antigravity",
    description="A TUI tool to manage SSH config files",
)
