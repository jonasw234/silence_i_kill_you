import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="silence_i_kill_you",
    version="0.0.1",
    author="Jonas A. Wendorf",
    description="Removes silence from video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonasw234/silence_i_kill_you",
    packages=setuptools.find_packages(),
    install_requires=["docopt", "moviepy"],
    include_package_data=True,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "OSI Approved :: GNU General Public License v3 or later (GPLv3)",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Video :: Conversion",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": ["silence_i_kill_you=silence_i_kill_you.silence_i_kill_you:main"],
    },
)
