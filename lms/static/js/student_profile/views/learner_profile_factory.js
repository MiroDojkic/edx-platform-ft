;(function (define, undefined) {
    'use strict';
    define([
        'gettext',
        'jquery',
        'underscore',
        'backbone',
        'logger',
        'edx-ui-toolkit/js/pagination/paging-collection',
        'js/student_account/models/user_account_model',
        'js/student_account/models/user_preferences_model',
        'js/views/fields',
        'js/student_profile/views/learner_profile_fields',
        'js/student_profile/views/learner_profile_view',
        'js/student_profile/models/badges_model',
        'js/student_profile/views/badge_list_container',
        'js/student_account/views/account_settings_fields',
        'js/views/message_banner',
        'string_utils'
    ], function (gettext, $, _, Backbone, Logger, PagingCollection, AccountSettingsModel, AccountPreferencesModel,
                 FieldsView, LearnerProfileFieldsView, LearnerProfileView, BadgeModel, BadgeListContainer,
                 AccountSettingsFieldViews, MessageBannerView) {

        return function (options) {

            var learnerProfileElement = $('.wrapper-profile');

            var accountSettingsModel = new AccountSettingsModel(
                _.extend(
                    options.account_settings_data,
                    {'default_public_account_fields': options.default_public_account_fields}
                ),
                {parse: true}
            );
            var AccountPreferencesModelWithDefaults = AccountPreferencesModel.extend({
                defaults: {
                    account_privacy: options.default_visibility
                }
            });
            var accountPreferencesModel = new AccountPreferencesModelWithDefaults(options.preferences_data);

            accountSettingsModel.url = options.accounts_api_url;
            accountPreferencesModel.url = options.preferences_api_url;

            var editable = options.own_profile ? 'toggle' : 'never';

            var messageView = new MessageBannerView({
                el: $('.message-banner')
            });

            var accountPrivacyFieldView = new LearnerProfileFieldsView.AccountPrivacyFieldView({
                model: accountPreferencesModel,
                required: true,
                editable: 'always',
                showMessages: false,
                title: interpolate_text(
                    gettext('{platform_name} learners can see my:'), {platform_name: options.platform_name}
                ),
                valueAttribute: "account_privacy",
                options: [
                    ['private', gettext('Limited Profile')],
                    ['all_users', gettext('Full Profile')]
                ],
                helpMessage: '',
                accountSettingsPageUrl: options.account_settings_page_url,
                persistChanges: true
            });

            var profileImageFieldView = new LearnerProfileFieldsView.ProfileImageFieldView({
                model: accountSettingsModel,
                valueAttribute: 'profile_image',
                editable: editable === 'toggle',
                messageView: messageView,
                imageMaxBytes: options['profile_image_max_bytes'],
                imageMinBytes: options['profile_image_min_bytes'],
                imageUploadUrl: options['profile_image_upload_url'],
                imageRemoveUrl: options['profile_image_remove_url']
            });

            var usernameFieldView = new FieldsView.ReadonlyFieldView({
                    model: accountSettingsModel,
                    screenReaderTitle: gettext('Username'),
                    valueAttribute: "username",
                    helpMessage: ""
            });

            var sectionOneFieldViews = [
                new FieldsView.TextareaFieldView({
                    model: accountSettingsModel,
                    messagePosition: 'header',
                    editable: editable,
                    persistChanges: true,
                    valueAttribute: 'email',
                    title: 'Email'
                }),
                new FieldsView.DropdownFieldView({
                    model: accountSettingsModel,
                    screenReaderTitle: gettext('Country'),
                    titleVisible: false,
                    required: true,
                    editable: editable,
                    showMessages: false,
                    iconName: 'fa-map-marker',
                    placeholderValue: gettext('Add Country'),
                    valueAttribute: "country",
                    options: options.country_options,
                    helpMessage: '',
                    persistChanges: true
                }),
                new AccountSettingsFieldViews.LanguageProficienciesFieldView({
                    model: accountSettingsModel,
                    screenReaderTitle: gettext('Preferred Language'),
                    titleVisible: false,
                    required: false,
                    editable: editable,
                    showMessages: false,
                    iconName: 'fa-comment',
                    placeholderValue: gettext('Add language'),
                    valueAttribute: "language_proficiencies",
                    options: options.language_options,
                    helpMessage: '',
                    persistChanges: true
                })
            ];

            var sectionTwoFieldViews = [
                // new FieldsView.TextareaFieldView({
                //     model: accountSettingsModel,
                //     editable: editable,
                //     showMessages: false,
                //     title: gettext('About me'),
                //     placeholderValue: gettext("Tell other learners a little about yourself: where you live, what your interests are, why you're taking courses, or what you hope to learn."),
                //     valueAttribute: "bio",
                //     helpMessage: '',
                //     persistChanges: true,
                //     messagePosition: 'header'
                // })
            ];

            var sectionTwoFreeTextFields = accountSettingsModel.attributes.account_privacy === 'private' ?
            {
                // TODO: define limited profile fields
            }
            :
            {
                name: 'Full Name',
                mailing_address: 'Street Address 1',
                secondary_address: 'Street Address 2',
                city: 'City',
                zipcode: 'Zip/Postal Code',
                company: 'Company',
                phone_number: 'Phone Number',
                title: 'Title',
                year_of_birth: 'Age',
                facebook_link: 'Facebook',
                linkedin_link: 'LinkedIn',
                twitter_link: 'Twitter'
            };

            var sectionTwoDropdownFields = accountSettingsModel.attributes.account_privacy === 'private' ?
            {
                // TODO: define limited profile fields
            }
            :
            {
                state: 'State',
                newsletter: 'Would you like to receive KF newsletter?',
                gender: 'Gender',
                bio: 'Your motivation...',
                immigrant_status: 'Were you born a citizen of the United States?',
                veteran_status: 'Have you ever served in any branch of the U.S. Armed Forces, including the Coast Guard, the National Guard, or Reserve component of any service branch? ',
                education: 'What was the highest degree or level of school you have completed?'
            };

            for (var key in sectionTwoFreeTextFields) {
                var value = sectionTwoFreeTextFields[key];
                sectionTwoFieldViews.push(
                    new FieldsView.TextareaFieldView({
                        model: accountSettingsModel,
                        messagePosition: 'header',
                        editable: editable,
                        persistChanges: true,
                        valueAttribute: key,
                        title: value
                    })
                );
            }

            for (var key in sectionTwoDropdownFields) {
                var value = sectionTwoDropdownFields[key];
                sectionTwoFieldViews.push(
                    new FieldsView.DropdownFieldView({
                        model: accountSettingsModel,
                        editable: editable,
                        showMessages: true,
                        placeholderValue: gettext('Add ' + value),
                        valueAttribute: key,
                        options: options[key + '_options'],
                        helpMessage: value,
                        persistChanges: true,
                        titleVisible: true,
                        title: value
                    })
                );
            }

            var BadgeCollection = PagingCollection.extend({
                queryParams: {
                    currentPage: 'current_page'
                }
            });
            var badgeCollection = new BadgeCollection();
            badgeCollection.url = options.badges_api_url;

            var badgeListContainer = new BadgeListContainer({
                'attributes': {'class': 'badge-set-display'},
                'collection': badgeCollection,
                'find_courses_url': options.find_courses_url,
                'ownProfile': options.own_profile,
                'badgeMeta': {
                    'badges_logo': options.badges_logo,
                    'backpack_ui_img': options.backpack_ui_img,
                    'badges_icon': options.badges_icon
                }
            });

            var learnerProfileView = new LearnerProfileView({
                el: learnerProfileElement,
                ownProfile: options.own_profile,
                has_preferences_access: options.has_preferences_access,
                accountSettingsModel: accountSettingsModel,
                preferencesModel: accountPreferencesModel,
                accountPrivacyFieldView: accountPrivacyFieldView,
                profileImageFieldView: profileImageFieldView,
                usernameFieldView: usernameFieldView,
                sectionOneFieldViews: sectionOneFieldViews,
                sectionTwoFieldViews: sectionTwoFieldViews,
                badgeListContainer: badgeListContainer
            });

            var getProfileVisibility = function() {
                if (options.has_preferences_access) {
                    return accountPreferencesModel.get('account_privacy');
                } else {
                    return accountSettingsModel.get('profile_is_public') ? 'all_users' : 'private';
                }
            };

            var showLearnerProfileView = function() {
                // Record that the profile page was viewed
                Logger.log('edx.user.settings.viewed', {
                    page: "profile",
                    visibility: getProfileVisibility(),
                    user_id: options.profile_user_id
                });

                // Render the view for the first time
                learnerProfileView.render();
            };

            if (options.has_preferences_access) {
                if (accountSettingsModel.get('requires_parental_consent')) {
                    accountPreferencesModel.set('account_privacy', 'private');
                }
            }
            showLearnerProfileView();

            return {
                accountSettingsModel: accountSettingsModel,
                accountPreferencesModel: accountPreferencesModel,
                learnerProfileView: learnerProfileView,
                badgeListContainer: badgeListContainer
            };
        };
    });
}).call(this, define || RequireJS.define);
