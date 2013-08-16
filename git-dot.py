#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function # for python 2 and stderr
from __version__ import version
import os
import sys
import getopt
from subprocess import check_output, call

# TODO use GitPython once it is compatible with python3
# instead of calling git(3)

program_name = 'git-dot'

def usage():
  print('''\
Usage: {0} [OPTION]... OUTPUT
Output a graph representing the Git history using the dot format
in the file OUTPUT.

-h, --help       display this help and exit
    --version    output version information and exit

With no FILE, or when FILE is -, read standard input.

Example:
{0} graph.dot                      Output the graph in graph.png
dot -Tpng -o graph.png graph.dot   using Graphviz.
'''.
format(program_name))

def show_version():
  print('''\
{} {}
Copyright (C) 2013 Benoît Legat.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by Benoît Legat.'''.format(program_name, version))

class Digraph:
  def __init__(self, file_name, graph_name):
    self.f = open(file_name, "w")
    self.f.write('digraph "{}" {{\n'.format(graph_name))

  def write_node(self, name, color, fillcolor, label):
    self.f.write('  "{}" [shape="box",style="rounded,filled",color="{}", fillcolor="{}", label="{}"];\n'.format(name, color, fillcolor, label))

  def link_nodes(self, name1, name2):
    self.f.write('  "{}" -> "{}";\n'.format(name1, name2))

  def close(self):
    self.f.write("}\n")
    self.f.close()


def git_log(log_format = None):
  return check_output(['git', 'log', '--all',
    '--pretty=format:{}'.format(log_format)], universal_newlines=True)

def cut_sha(sha):
  return sha[0:5]

def get_content(file_name):
  f = open(file_name, "r")
  content = f.read()
  f.close()
  return content.strip()

def get_refs(name):
  folder = os.path.join('.git', os.path.join('refs', name))
  refs = os.listdir(folder)
  dic = []
  for ref in refs:
    dic.append((ref,
      cut_sha(get_content(os.path.join(folder, ref)))))
  return dic

def create_graph(file_name):
  graph = Digraph(file_name, "git history")

  # Branches
  for branch, sha in get_refs("heads"):
    graph.write_node(branch, "indianred4", "lightpink", branch)
    graph.link_nodes(branch, sha)

  # Tags
  for tag, sha in get_refs("tags"):
    graph.write_node(tag, "seagreen", "palegreen", tag)
    graph.link_nodes(tag, sha)

  # HEAD
  graph.write_node("HEAD", "seagreen", "khaki1", "HEAD")
  head = get_content(os.path.join('.git', 'HEAD'))
  if head[:5] == 'ref: ':
    # 'ref: refs/heads/<current_branch>'
    graph.link_nodes("HEAD", head[16:])
  else:
    graph.link_nodes("HEAD", cut_sha(head))

  # Commits
  for full_sha, title, parents in zip(
      git_log('%H').split(),
      git_log('%s').split('\n'),
      git_log('%P').split('\n')):
    sha = cut_sha(full_sha)
    graph.write_node(sha, "skyblue4", "slategray1",
    '{}\\n{}'.format(sha,title))
    for parent in parents.split():
      graph.link_nodes(sha, cut_sha(parent))

  graph.close()

def print_err(message):
  print("{0}: {1}".format(program_name, message),
      file = sys.stderr)

def main():
  try:
    # gnu_getopt allow opts to be after args. For
    # $ git-dot.py config.yml -v
    # gnu_getopt will consider -v as an option and getopt
    # will see it as an arg like config.yml
    opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
        ["help", "version"])
  except getopt.GetoptError as err:
    print_err(str(err))
    usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h", "--help"):
      usage()
      sys.exit()
    elif o == "--version":
      show_version()
      sys.exit()
    else:
      assert False, "unhandled option"

  if not args:
    print_err("Missing output file")
    exit(-1)

  create_graph(args[0])

if __name__ == "__main__":
    main()
