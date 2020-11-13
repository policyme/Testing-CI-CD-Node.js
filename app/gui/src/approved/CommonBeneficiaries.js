import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import css from 'styled-jsx/css';

import { nextQuestion } from '../../Actions/session';

import Button from '../../components/Button';
import Heading from '../../components/Heading';
import SecureFooter from '../../components/SecureFooter';

const CommonBeneficiaries = (props) => {
  const handleChooseMyOwn = () => {
    props.nextQuestion();
  };
  const handleUseThisOption = () => {
    props.nextQuestion();
  };
  return (
    <div className="beneficiaries-container">
      <Heading level={1}>
        Would you like to use the most common beneficiary option?
      </Heading>
      <p>
        Your beneficiaries are the people who will collect your
        life insurance payout if you pass away.
        You can always change them later.
      </p>
      <Heading level={2} headingStyle={4}>
        Your death benefit would pay out as follows:
      </Heading>
      <div className="numberRow">
        <span className="numberCircle">1</span>
        <p>
          To your <b>spouse</b>
        </p>
      </div>
      <div className="line" />
      <Heading level={2} headingStyle={4}>
        If you don’t have a living spouse at the time of your death:
      </Heading>
      <div className="numberRow">
        <span className="numberCircle">2</span>
        <p>
          Divided equally between your <b>children</b>, including step-children and adopted children
        </p>
      </div>
      <div className="line" />
      <Heading level={2} headingStyle={4}>
        If you don’t have living children at the time of your death:
      </Heading>
      <div className="numberRow">
        <span className="numberCircle">3</span>
        <p>
          Divided equally between your <b>parent(s)</b>
        </p>
      </div>
      <p>
        If none of the above are applicable, your payout will be made to your estate.
      </p>
      <Button
        className="btn btn-secondary"
        type="button"
        onClick={handleChooseMyOwn}
      >
        Choose My Own
      </Button>
      <Button
        className="btn btn-primary"
        type="button"
        onClick={handleUseThisOption}
      >
        Use this Option
      </Button>
      {/* TODO: add Progress Component */}
      <SecureFooter />
      <style jsx>{styles}</style>
    </div>
  );
};

const styles = css`
@import "../../styles/utilities/breakpoints.sass";
@import "../../styles/utilities/variables.sass";
.beneficiaries-container {
  max-width: 43rem;
  margin: auto;
}

.beneficiaries-container > :global(*) {
  margin-bottom: 1.75rem;
}

p {
  text-align: center;
  max-width: 20rem;
  @media #{$md-up} {
    max-width: 40rem;
    margin: auto 1.5rem;
  }
}

.numberRow {
  display: flex;
  margin: auto 1.5rem;
}

.numberRow > p {
  margin-left: 0;
  text-align: left;
}

.numberCircle {
  border-radius: 50%;
  min-width: 2.25em;
  height: 2.25rem;
  line-height: 2rem;
  border: solid 0.125rem $prussian-blue;
  text-align: center;
  color: $prussian-blue;
  margin-right: 0.5rem;

  @media #{$md-up} {
    margin-left: 1.25rem;
    margin-right: 1rem;
  }
}

.line {
  border-top: solid 0.0625rem $border-blue;
  margin: 1rem 1.5rem;
  max-width: 20rem;
  @media #{$md-up} {
    max-width: 40rem;
    margin: 1.5rem;
  }
}

:global(.h4) {
  margin-left: 2rem;
  margin-right: 2rem;
}

`;

CommonBeneficiaries.propTypes = {
};

CommonBeneficiaries.defaultProps = {
};

const mapDispatchToProps = {
  nextQuestion,
};

const mapStateToProps = state => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(CommonBeneficiaries);
