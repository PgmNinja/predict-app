import React from 'react';
import * as ReactBootStrap from 'react-bootstrap'

const Spinner = () => {
  return <div className='spinner'>

  <ReactBootStrap.Spinner animation="border" size="sm" />
  <ReactBootStrap.Spinner animation="border" />
  <ReactBootStrap.Spinner animation="grow" size="sm" />
  <ReactBootStrap.Spinner animation="grow" />

  </div>;
};

export default Spinner;
