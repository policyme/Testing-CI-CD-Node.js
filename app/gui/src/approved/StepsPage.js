import React, { useState } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import css from 'styled-jsx/css';

import Expandable from '../../components/Expandable';
import GetSupport from '../../components/GetSupport';
import Heading from '../../components/Heading';
import HighlightToolTip from '../../components/HighlightToolTip';
import IconListItem from '../../components/IconListItem';
import MultiStepComponent from '../../components/MultiStepComponent';
import SecureFooter from '../../components/SecureFooter';
import { TOOLTIP_MESSAGES } from '../../utils/const';
import { nextQuestion } from '../../Actions/session';

import BENE from '../../static/images/steps/Icon_Beneficiaries.svg';
import BENECOMPLETE from '../../static/images/steps/Icon_Beneficiaries_Complete.svg';
import BLUE_CHECKMARK from '../../static/images/Icon_BlueCheckmark.svg';
import GREY_X from '../../static/images/Icon_GreyX.svg';
import PAYMENT from '../../static/images/steps/Icon_Payment.svg';
import PAYMENTCOMPLETE from '../../static/images/steps/Icon_Payment_Complete.svg';
import REVIEWPOLICY from '../../static/images/steps/Icon_ReviewPolicy.svg';
import REVIEWPOLICYCOMPLETE from '../../static/images/steps/Icon_ReviewPolicy_Complete.svg';
import VERIFYID from '../../static/images/steps/Icon_VerifyID.svg';
import VERIFYIDCOMPLETE from '../../static/images/steps/Icon_VerifyID_Complete.svg';

const MyPolicyComponent = () => (
  <div className="my-policy-container">
    <Expandable
      headerText={`My policy summary`}
      mixpanelOpenEventName={`TODO: add mixpanel event`}
    >
      <span className="list-title">
        What’s included:
      </span>
      <ul className="with-icons">
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          All causes of death are included except for suicide in the
          first two years of your policy term
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          One lump-sum, tax-free death benefit to your beneficiaries
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          Rate will never change, no matter what happens to your health
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          30-day grace period for missed payments without losing your coverage
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          Cancel anytime without fees or penalties
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          Free 30-day trial period
        </IconListItem>
        <IconListItem icon={<img alt="checkmark" src={BLUE_CHECKMARK} />}>
          All payments will be fully refunded if you cancel within 30 days
        </IconListItem>
      </ul>
      <span className="list-title">
        What’s not included:
      </span>
      <ul className="with-icons">
        <IconListItem icon={<img alt="checkmark" src={GREY_X} />}>
          Suicide in the first two years of your policy term is the only cause of death
          not included (this is industry standard).
          In this case, payments will be limited to premiums paid.
        </IconListItem>
      </ul>
      <span className="list-title">
        How to make a claim:
      </span>
      <p>
        Have your beneficiaries get in touch with us by email at {}
        <a href="mailto:advisor@policyme.com">advisor@policyme.com</a> {}
        or phone at 1.866.999.7457.
        We’ll take care of the rest and will help your beneficiary in obtaining the
        death certificate needed to receive the payout.
      </p>
      <span className="list-title">
        How to make changes to your policy:
      </span>
      <p>
        Get in touch with us by sending an email to {}
        <a href="mailto:advisor@policyme.com">advisor@policyme.com</a> {}
        or giving us a call at 1.866.999.7457. We will be happy to assist you.
      </p>
    </Expandable>
    <style jsx>{`
      @import "../../styles/utilities/breakpoints.sass";
      @import "../../styles/utilities/variables.sass";
      .my-policy-container :global(span.text) {
        text-align: left;
        font-weight: bold;
        line-height: 1.3;
        color: $prussian-blue;

        font-size: 1.125rem;
        @media #{$md-up} {
          font-size: 1.375rem;
        }
      }

      span.list-title {
        text-align: left;
        font-weight: bold;
        line-height: 1.3;
        color: $prussian-blue;
      
        font-size: 1.125rem;
        @media #{$md-up} {
          font-size: 1.25rem;
        }
      }
      
      .my-policy-container :global(ul.with-icons) {
        padding-left: 0;
      }
      
      .my-policy-container :global(.with-icons li) {
        list-style: none;
        margin-bottom: 1rem;
        &:last-child {
          margin-bottom: 2rem;

          @media #{$md-up} {
            margin-bottom: 2.5rem;
          }
        }
      }

      p {
        margin-top: 1rem;
        margin-bottom: 2rem;
        @media #{$md-up} {
          margin-bottom: 2.5rem;
        }
        &:last-child {
          margin-bottom: 0rem;
        }
      }
    `}</style>
  </div>
);

const stepsData = [
  {
    key: `0`,
    title: 'Select your beneficiaries',
    desc: 'Choose the people who will collect the insurance payout if you were to pass away.',
    buttonText: 'Select My Beneficiaries',
    icon: BENE,
    completedIcon: BENECOMPLETE,
  },
  {
    key: `1`,
    title: 'Verify your identity',
    desc: 'Upload photos of your government-issued ID to our secure portal.Please note this process requires a cell phone - make sure to have it nearby!',
    buttonText: 'Verify My ID',
    icon: VERIFYID,
    completedIcon: VERIFYIDCOMPLETE,
  },
  {
    key: `2`,
    title: 'Review & eSign your policy',
    desc: 'Review your policy documents and sign-off to accept your coverage.',
    buttonText: 'Review & eSign My Policy',
    icon: REVIEWPOLICY,
    completedIcon: REVIEWPOLICYCOMPLETE,
  },
  {
    key: `3`,
    title: 'Add your payment details',
    desc: 'Choose either a monthly or annual payment plan and add your credit card information.',
    buttonText: 'Add My Payment Details',
    icon: PAYMENT,
    completedIcon: PAYMENTCOMPLETE,
  },
];

const StepsPage = (props) => {
  const {
    monthlyCost, formattedCoverageAmt, term,
  } = props;
  // TODO: remove stepCounter & its logic
  // these should be changed when we implement the logic
  const [stepCounter, setStepCounter] = useState(1);
  const handleClick = () => {
    setStepCounter(stepCounter + 1);
    props.nextQuestion();
  };

  const stepList = [];
  stepsData.forEach(stepData => {
    const moreData = {
      onClick: handleClick,
    };
    stepList.push({ ...stepData, ...moreData });
  });

  return (
    <div className="approved-step-container">
      <Heading level={1}>
        {`You've been approved!`}
      </Heading>
      <div className="line" />
      <div className="step-title">
        {`Your final rate is `}
        <HighlightToolTip
          mixpanelEvent="TODO: add mixpanel event"
          tooltipContent={monthlyCost}
          showModal
        >
          {TOOLTIP_MESSAGES.MONTHLY_RATE_MESSAGE}
        </HighlightToolTip>
        {` for `}
        <HighlightToolTip
          mixpanelEvent="TODO: add mixpanel event"
          tooltipContent={formattedCoverageAmt}
          showModal
        >
          {TOOLTIP_MESSAGES.COVERAGE_AMOUNT_STANDALONE_MESSAGE}
        </HighlightToolTip>
        {` in coverage over a `}
        <HighlightToolTip
          mixpanelEvent="TODO: add mixpanel event"
          tooltipContent={`${term}-year`}
          showModal
        >
          {TOOLTIP_MESSAGES.TERM_LENGTH_STANDALONE_MESSAGE}
        </HighlightToolTip>
        {` policy term.`}
      </div>
      <div className="step-body">
        <Heading level={2} headingStyle={3}>
          {`Activate your coverage in ${stepList.length} steps:`}
        </Heading>
        <MultiStepComponent
          stepList={stepList}
          currentStep={stepCounter}
        />
        <GetSupport />
        <MyPolicyComponent />
      </div>
      <SecureFooter />
      <style jsx>{styles}</style>
    </div>
  );
};

const styles = css`
@import "../../styles/utilities/breakpoints.sass";
@import "../../styles/utilities/variables.sass";

.approved-step-container {
  max-width: 45rem;
  margin: auto;
}

.approved-step-container :global(.h1) {
  margin-bottom: 0rem;
}

.approved-step-container :global(.h2) {
  padding: 0rem 3rem;
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

.step-title {
  display: flex;
  justify-content: center;
  flex-flow: row wrap;
  color: $prussian-blue;
  font-weight: bold;
  margin: 0rem auto 2.5rem auto;
  line-height: 2rem;
  padding: 0 1rem;
  font-size: 1.125rem;
  letter-spacing: -0.0225rem;

  @media #{$sm-up} {
    padding: 0 1.5rem;
    font-size: 1.25rem;
    letter-spacing: -0.025rem;
    margin-bottom: 3rem;
  }
}
`;

StepsPage.propTypes = {
  monthlyCost: PropTypes.string.isRequired,
  formattedCoverageAmt: PropTypes.string.isRequired,
  term: PropTypes.number.isRequired,
};

StepsPage.defaultProps = {
};

const mapDispatchToProps = {
  nextQuestion,
};

// TODO: change these once we implement them
const mapStateToProps = state => ({
  monthlyCost: '$78.83 / month',
  formattedCoverageAmt: '$600,000',
  term: 20,
});

export default connect(mapStateToProps, mapDispatchToProps)(StepsPage);
