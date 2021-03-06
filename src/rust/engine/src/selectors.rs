// Copyright 2017 Pants project contributors (see CONTRIBUTORS.md).
// Licensed under the Apache License, Version 2.0 (see LICENSE).

use core::{Field, Key, TypeConstraint, TypeId};

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct Select {
  pub product: TypeConstraint,
  pub variant_key: Option<String>,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct SelectDependencies {
  pub product: TypeConstraint,
  pub dep_product: TypeConstraint,
  pub field: Field,
  pub field_types: Vec<TypeId>,
  pub transitive: bool,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct SelectProjection {
  pub product: TypeConstraint,
  // TODO: This should in theory be a TypeConstraint, but because the `project` operation
  // needs to construct an instance of the type if the result doesn't match, we use
  // a concrete type here.
  pub projected_subject: TypeId,
  pub field: Field,
  pub input_product: TypeConstraint,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub struct SelectLiteral {
  pub subject: Key,
  pub product: TypeConstraint,
}

#[derive(Clone, Debug, Eq, Hash, PartialEq)]
pub enum Selector {
  Select(Select),
  SelectDependencies(SelectDependencies),
  SelectProjection(SelectProjection),
  SelectLiteral(SelectLiteral),
}

impl Selector {
  pub fn select(product: TypeConstraint) -> Selector {
    Selector::Select(
      Select {
        product: product,
        variant_key: None,
      }
    )
  }
}
