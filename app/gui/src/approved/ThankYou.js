import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import css from 'styled-jsx/css';

import GetSupport from '../../components/GetSupport';
import Heading from '../../components/Heading';
import HighlightToolTip from '../../components/HighlightToolTip';
import SecureFooter from '../../components/SecureFooter';
import WithWindowSize from '../../components/HOC/WithWindowSize';

import { TOOLTIP_MESSAGES } from '../../utils/const';

import SUCCESS from '../../static/images/IconSuccess.svg';

const ThankYou = (props) => {
  const { years, coverageAmt, annualPayment, isMdUp } = props;
  return (
    <div className="approved-thankyou-container">
      <img src={SUCCESS} alt="success" />
      <Heading level={1}>
        Thank you for your payment!
      </Heading>
      <p>
        Check your email for a confirmation of your payment and policy documents.
      </p>
      <div className="policy-component">
        <Heading level={2} headingStyle={3}>
          Your policy is now in effect
        </Heading>
        <div className="line" />
        <div className="policy-details">
          {`If you pass away in the next `}
          <HighlightToolTip
            mixpanelEvent="TODO: add mixpanel event"
            tooltipContent={`${years},`}
            showModal
          >
            {TOOLTIP_MESSAGES.TERM_LENGTH_STANDALONE_MESSAGE}
          </HighlightToolTip>
          &nbsp;{` your loved ones will receive `}
          <HighlightToolTip
            mixpanelEvent="TODO: add mixpanel event"
            tooltipContent={coverageAmt}
            showModal
          >
            {TOOLTIP_MESSAGES.COVERAGE_AMOUNT_STANDALONE_MESSAGE}
          </HighlightToolTip>
          &nbsp;{` in a tax-free death benefit. `}
          <div className="line-break" />
          {!isMdUp && <div className="spacing" />}
          {`Your annual payment will be `}
          <HighlightToolTip
            mixpanelEvent="TODO: add mixpanel event"
            tooltipContent={annualPayment}
            showModal
          >
            {TOOLTIP_MESSAGES.MONTHLY_RATE_MESSAGE}
          </HighlightToolTip>
          {`.`}
        </div>
      </div>
      <GetSupport />
      <SecureFooter />
      <style jsx>{styles}</style>
    </div>
  );
};

const styles = css`
@import "../../styles/utilities/breakpoints.sass";
@import "../../styles/utilities/variables.sass";

.approved-thankyou-container {
  max-width: 45rem;
  margin: auto;
  text-align: center;
}

.line {
  border-top: solid 0.063rem $border-blue;
  margin: 1rem 1.5rem;
  padding: 0 1rem;
  @media #{$md-up} {
    padding: 0 1.5rem;
    margin: 1.5rem;
  }
}

.policy-component {
  border: solid 0.0625rem $border-blue;
  border-radius: 0.25rem;

  padding: 1.5rem;
  margin: 1rem auto;

  @media #{$sm-up} {
    padding: 2rem 1.5rem;
    margin: 1.5rem auto;
  }
}

.policy-details {
  display: flex;
  justify-content: center;
  flex-flow: row wrap;
  color: $prussian-blue;
  margin: 0;
  line-height: 1.5rem;

  font-size: 1rem;
  letter-spacing: -0.0225rem;

  @media #{$md-up} {
    font-size: 1.25rem;
    letter-spacing: -0.025rem;
    margin: 0 1rem;
    line-height: 2.5rem;
  }
}

.line-break {
  flex-basis: 100%;
  height: 0;
}

.spacing {
  margin-bottom: 1.125rem;
}

.policy-details :global(.tooltip-link) {
  margin-right: 0;
  font-size: 1.125rem;
  @media #{$md-up} {
    font-size: 1.875rem;
  }
}
`;

ThankYou.propTypes = {
  years: PropTypes.string.isRequired,
  coverageAmt: PropTypes.string.isRequired,
  annualPayment: PropTypes.string.isRequired,
};

ThankYou.defaultProps = {
};

const mapDispatchToProps = {
};

// TODO: change these once we implement them
const mapStateToProps = state => ({
  years: '20 years',
  coverageAmt: '$600,000',
  annualPayment: '$851.34',
});

export default connect(mapStateToProps, mapDispatchToProps)(WithWindowSize(ThankYou));
