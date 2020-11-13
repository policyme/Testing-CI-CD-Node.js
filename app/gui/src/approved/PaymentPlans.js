import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import css from 'styled-jsx/css';

import Expandable from '../../components/Expandable';
import Form from '../../components/Form';
import Heading from '../../components/Heading';
import SecureFooter from '../../components/SecureFooter';

const PaymentPlans = (props) => {
  const handleNext = () => {
    // TODO: logic for choosing Plan
  };
  return (
    <Form
      onSubmit={() => handleNext()}
      name="Payment"
      disableSlide={props.backPressed}
      className="wide"
      start="0rem"
      end="1.75rem"
    >
      <Heading level={1}>
        Please choose your payment plan
      </Heading>
      <p className="center">Recurring billing, cancel anytime</p>
      {/* TODO: add Payment Components */}
      <Expandable
        headerText={`How does payment work?`}
        mixpanelOpenEventName={`TODO: add mixpanel event`}
      >
        <p>
          We accept credit cards as the standard form of payment for your insurance plan.
          You will be asked to provide standard credit card details
          on the following page after you select a monthly or annual payment plan.
        </p>
        <p>
          For monthly payments, we would charge the indicated rate every month at the same time.
          For annual payments, we would only charge the indicated amount
          to your credit card in a one-time payment every year.
        </p>
        <p>
          All payments are securely processed through Driasi to ensure your data is protected.
        </p>
      </Expandable>
      <Expandable
        headerText={`When is the first payment charged?`}
        mixpanelOpenEventName={`TODO: add mixpanel event`}
      >
        <p>
          Your first payment will be charged within 24 hours
          after you have provided PolicyMe with your credit card details.
        </p>
      </Expandable>
      {/* TODO: add Progress Component */}
      <SecureFooter />
      <style jsx>{styles}</style>
    </Form>
  );
};

const styles = css`
@import "../../styles/utilities/breakpoints.sass";
@import "../../styles/utilities/variables.sass";
.center {
  text-align: center;
}
p {
  margin-bottom: 1rem;
} 
`;

PaymentPlans.propTypes = {
};

PaymentPlans.defaultProps = {
};

const mapDispatchToProps = {
};

const mapStateToProps = state => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(PaymentPlans);
