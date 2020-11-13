import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import css from 'styled-jsx/css';

import Button from '../../components/Button';
import Expandable from '../../components/Expandable';
import Form from '../../components/Form';
import GetSupport from '../../components/GetSupport';
import Heading from '../../components/Heading';
import SecureFooter from '../../components/SecureFooter';

const ReviewESignPolicy = (props) => {
  const handleNext = () => {
    // TODO: logic for eSigning App
  };
  return (
    <Form
      onSubmit={() => handleNext()}
      name="eSignPolicy"
      disableSlide={props.backPressed}
      className="wide"
      start="0rem"
      end="1.75rem"
    >
      <Heading level={1}>
        Please review and eSign your policy
      </Heading>
      <p className="center">
        Press the “eSign My Application” button to review and
        eSign your policy documents on DocuSign.
      </p>
      <Button
        className="btn btn-primary"
        type="submit"
      >
        eSign My Application
      </Button>
      {/* TODO: add Progress Component */}
      <GetSupport />
      <Expandable
        headerText={`What am I eSigning?`}
        mixpanelOpenEventName={`TODO: add mixpanel event`}
      >
        <p>
          The policy documents that you are eSigning include all of the information
          you submitted to PolicyMe in your online application as well as the terms of your policy.
        </p>
        <p>
          By eSigning, you will be confirming that you accept the coverage.
          If you would like to go over your policy documents with an advisor,
          click on the “Get Support” button above.
        </p>
      </Expandable>
      <Expandable
        headerText={`What happens after I eSign?`}
        mixpanelOpenEventName={`TODO: add mixpanel event`}
      >
        <p>
          After you eSign, the only step left will be to add your payment details.
          Once your first payment is processed, you will receive an email confirmation
          with a copy of all your policy documents and your policy will come into effect.
        </p>
      </Expandable>
      <Expandable
        headerText={`How do I change an answer in my application?`}
        mixpanelOpenEventName={`TODO: add mixpanel event`}
      >
        <p>
          If you made a mistake or forgot to include something in your application,
          give us a call at 1.866.999.7457 or send an email to <a href="mailto:advisor@policyme.com">advisor@policyme.com</a>.
          We will be happy to assist you.
        </p>
      </Expandable>
      <SecureFooter />
      <style jsx>{styles}</style>
    </Form>
  );
};

const styles = css`
@import "../../styles/utilities/breakpoints.sass";
@import "../../styles/utilities/variables.sass";

p.center {
  text-align: center;
  max-width: 34rem;
}
`;

ReviewESignPolicy.propTypes = {
};

ReviewESignPolicy.defaultProps = {
};

const mapDispatchToProps = {
};

const mapStateToProps = state => ({
});

export default connect(mapStateToProps, mapDispatchToProps)(ReviewESignPolicy);
