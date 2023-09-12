CREATE TABLE PaymentMethods (
  PaymentMethodID int PRIMARY KEY,
  PaymentMethod varchar(255)
);

CREATE TABLE CardBrands (
  CardBrandID int PRIMARY KEY,
  CardBrand varchar(255)
);

CREATE TABLE Countries (
  CountryID int PRIMARY KEY,
  Country varchar(255)
);

CREATE TABLE DeviceTypes (
  DeviceTypeID int PRIMARY KEY,
  DeviceType varchar(255)
);

CREATE TABLE CustomerSegments (
  CustomerSegmentID int PRIMARY KEY,
  CustomerSegment varchar(255)
);

CREATE TABLE Channels (
  ChannelID int PRIMARY KEY,
  ChannelType varchar(255)
);

CREATE TABLE IndividualTransactions (
  TransactionID int PRIMARY KEY,
  Amount decimal,
  Date date,
  Status varchar(255),
  MerchantLocationID int,
  TerminalID int,
  ChannelID int
);

CREATE TABLE BatchTransactions (
  BatchID int PRIMARY KEY,
  Date date,
  TotalTransactionAmount decimal,
  AverageTransactionValue decimal,
  SuccessfulTransactions int,
  FailedTransactions int,
  RefundedTransactions int,
  ChargebackCount int,
  AverageAuthorizationTime time,
  AverageSettlementTime time,
  MerchantLocationID int,
  ChannelID int
);

CREATE TABLE Merchants (
  MerchantID int PRIMARY KEY,
  MerchantName varchar(255),
  Address varchar(255),
  City varchar(255),
  State varchar(255),
  Zip varchar(255),
  IsEcom boolean,
  IsMOTO boolean
);

CREATE TABLE MerchantLocations (
  MerchantLocationID int PRIMARY KEY,
  MerchantID int,
  Address varchar(255),
  City varchar(255),
  State varchar(255),
  Zip varchar(255),
  NumberOfTerminals int
);

CREATE TABLE CardTerminals (
  TerminalID int PRIMARY KEY,
  MerchantLocationID int,
  TerminalType varchar(255)
);

CREATE TABLE Settlements (
  SettlementID int PRIMARY KEY,
  BatchID int,
  SettlementDate date,
  TotalSettlementAmount decimal,
  BatchTotals text,
  InterchangeFees decimal,
  DiscountRates decimal,
  ReserveAmount decimal,
  ClearedFunds decimal,
  ReturnedFunds decimal,
  NetSettlementAmount decimal,
  SettlementCurrency varchar(255),
  SettlementStatus varchar(255),
  SettlementDelay int,
  ReserveReleaseDate date
);

CREATE TABLE Reconciliation (
  ReconciliationID int PRIMARY KEY,
  BatchID int,
  ReconciliationDate date,
  DiscrepancyCount int,
  DiscrepancyAmount decimal,
  UnsettledTransactions int,
  UnsettledAmount decimal,
  ReconciliationStatus varchar(255)
);

CREATE TABLE Fees (
  FeeID int PRIMARY KEY,
  TransactionID int,
  ReportDate date,
  TotalFees decimal,
  DiscountFees decimal,
  TransactionFees decimal,
  MonthlyFees decimal,
  ChargebackFees decimal,
  OtherFees text,
  FeeDetails text,
  AverageFeePerTransaction decimal
);

CREATE TABLE Transaction_PaymentMethods (
  TransactionID int,
  PaymentMethodID int
);

CREATE TABLE Transaction_CardBrands (
  TransactionID int,
  CardBrandID int
);

CREATE TABLE Transaction_Countries (
  TransactionID int,
  CountryID int
);

CREATE TABLE Transaction_DeviceTypes (
  TransactionID int,
  DeviceTypeID int
);

CREATE TABLE Transaction_CustomerSegments (
  TransactionID int,
  CustomerSegmentID int
);

ALTER TABLE IndividualTransactions ADD FOREIGN KEY (MerchantLocationID) REFERENCES MerchantLocations (MerchantLocationID);

ALTER TABLE BatchTransactions ADD FOREIGN KEY (MerchantLocationID) REFERENCES MerchantLocations (MerchantLocationID);

ALTER TABLE MerchantLocations ADD FOREIGN KEY (MerchantID) REFERENCES Merchants (MerchantID);

ALTER TABLE CardTerminals ADD FOREIGN KEY (MerchantLocationID) REFERENCES MerchantLocations (MerchantLocationID);

ALTER TABLE Settlements ADD FOREIGN KEY (BatchID) REFERENCES BatchTransactions (BatchID);

ALTER TABLE Reconciliation ADD FOREIGN KEY (BatchID) REFERENCES BatchTransactions (BatchID);

ALTER TABLE Fees ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE IndividualTransactions ADD FOREIGN KEY (ChannelID) REFERENCES Channels (ChannelID);

ALTER TABLE BatchTransactions ADD FOREIGN KEY (ChannelID) REFERENCES Channels (ChannelID);

ALTER TABLE Transaction_PaymentMethods ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE Transaction_PaymentMethods ADD FOREIGN KEY (PaymentMethodID) REFERENCES PaymentMethods (PaymentMethodID);

ALTER TABLE Transaction_CardBrands ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE Transaction_CardBrands ADD FOREIGN KEY (CardBrandID) REFERENCES CardBrands (CardBrandID);

ALTER TABLE Transaction_Countries ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE Transaction_Countries ADD FOREIGN KEY (CountryID) REFERENCES Countries (CountryID);

ALTER TABLE Transaction_DeviceTypes ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE Transaction_DeviceTypes ADD FOREIGN KEY (DeviceTypeID) REFERENCES DeviceTypes (DeviceTypeID);

ALTER TABLE Transaction_CustomerSegments ADD FOREIGN KEY (TransactionID) REFERENCES IndividualTransactions (TransactionID);

ALTER TABLE Transaction_CustomerSegments ADD FOREIGN KEY (CustomerSegmentID) REFERENCES CustomerSegments (CustomerSegmentID);
