# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import unittest

from pants.backend.jvm.targets.exclude import Exclude
from pants.backend.jvm.targets.jar_dependency import JarDependency
from pants.backend.jvm.targets.scala_jar_dependency import ScalaJarDependency


class JarDependencyTest(unittest.TestCase):

  def test_jar_dependency_excludes_change_hash(self):
    with_excludes = self._mkjardep()
    without_excludes = self._mkjardep(excludes=[])
    self.assertNotEqual(with_excludes.cache_key(), without_excludes.cache_key())

  def test_jar_dependency_copy(self):
    self._test_copy(self._mkjardep())

  def test_scala_jar_dependency_copy(self):
    self._test_copy(self._mkjardep(tpe=ScalaJarDependency))

  def test_get_url(self):
    """Test using relative url and absolute url are equivalent."""
    abs_url = 'file:///a/b/c'
    rel_url = 'file:c'
    base_path = '/a/b'

    jar_with_rel_url = self._mkjardep(url=rel_url, base_path=base_path)
    self.assertEquals(abs_url, jar_with_rel_url.get_url())
    self.assertEquals(rel_url, jar_with_rel_url.get_url(relative=True))

    jar_with_abs_url = self._mkjardep(url=abs_url, base_path=base_path)
    self.assertEquals(abs_url, jar_with_abs_url.get_url())
    self.assertEquals(rel_url, jar_with_abs_url.get_url(relative=True))

  def _test_copy(self, original):
    # A no-op clone results in an equal object.
    self.assertEqual(original, original.copy())
    # Excludes included in equality.
    excludes_added = original.copy(excludes=[Exclude(org='com.blah', name='blah')])
    self.assertNotEqual(original, excludes_added)
    # Clones are equal with equal content.
    self.assertEqual(original.copy(rev='1.2.3'), original.copy(rev='1.2.3'))

  def _mkjardep(self, org='foo', name='foo',
                excludes=(Exclude(org='example.com', name='foo-lib'),), tpe=JarDependency,
                **kwargs):
    return tpe(org=org, name=name, excludes=excludes, **kwargs)
