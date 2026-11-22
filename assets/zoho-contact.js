function addAriaSelected1011088000000647216(){
									var optionElem = event.target;
									var previousSelectedOption = optionElem.querySelector('[aria-selected=true]');
									if (previousSelectedOption) {
										previousSelectedOption.removeAttribute('aria-selected');
									}
									optionElem.querySelectorAll('option') [optionElem.selectedIndex] .ariaSelected = 'true';
								}
								function privacyAlert1011088000000647216(){
									var privacyTool = document.getElementById('privacyTool1011088000000647216');
									var privacyErr = document.getElementById('privacyErr1011088000000647216');
									if (privacyTool != undefined && !privacyTool.checked) {
										privacyErr.style.visibility = 'visible';
										privacyTool.ariaInvalid = 'true';
										privacyTool.focus();
										return false;
									}
									return true;
								}
								function disableErr1011088000000647216(){
									var privacyTool = document.getElementById('privacyTool1011088000000647216');
									var privacyErr = document.getElementById('privacyErr1011088000000647216');
									if (privacyTool != undefined && privacyTool.checked && privacyErr != undefined) {
										privacyErr.style.visibility = 'hidden';
										privacyTool.ariaInvalid = 'false';
									}
								}
								function validateEmail1011088000000647216(){
									var form = document.forms['WebToLeads1011088000000647216'];
									var emailFld = form.querySelectorAll('[ftype=email]');
									var i;
									for(i = 0; i < emailFld.length; i++ ) {
										var emailVal = emailFld[i].value;
										if ((emailVal.replace (/^\s+|\s+$/g,'') ) .length != 0) {
											var atpos = emailVal.indexOf('@');
											var dotpos = emailVal.lastIndexOf('.');
											if(atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= emailVal.length) {
												alert('Veuillez entrer une adresse e-mail valide. ');
												emailFld[i].focus();
												return false;
											}
										}
									}
									return true;
								}
								function checkMandatory1011088000000647216(isAjax){
									var mndFileds = new Array('Company', 'First Name', 'Last Name', 'Email', 'Phone');
									var fldLangVal = new Array('Société', 'Prénom', 'Nom', 'E\-mail', 'Téléphone');
									for (i = 0; i < mndFileds.length; i++ ) {
										var fieldObj = document.forms['WebToLeads1011088000000647216'] [mndFileds[i]];
										if (fieldObj) {
											if(((fieldObj.value) .replace (/^\s+|\s+$/g,'') ) .length == 0) {
												if (fieldObj.type == 'file') {
													alert('Veuillez sélectionner un fichier à charger.');
													fieldObj.focus();
													return false;
												}
												alert(fldLangVal[i] + ' ne peut pas être vide.');
												fieldObj.focus();
												return false;
											} else if (fieldObj.nodeName == 'SELECT') {
												if (fieldObj.options[fieldObj.selectedIndex].value == '-None-') {
													alert(fldLangVal[i] + ' ne peut être aucun.');
													fieldObj.focus();
													return false;
												}
											} else if (fieldObj.type == 'checkbox') {
												if (fieldObj.checked == false) {
													alert('Please accept  ' + fldLangVal[i]);
													fieldObj.focus();
													return false;
												}
											}
											try{
												if (fieldObj.name == 'Last Name') {
													name = fieldObj.value;
												}
											} catch (e){}
										}
									}
									if ( !validateEmail1011088000000647216 () ) {
										return false;
									}
									if ( !privacyAlert1011088000000647216 () ) {
										return false;
									}
									var urlparams = new URLSearchParams(window.location.search);
									if (urlparams.has ('service') && (urlparams.get ('service') === 'smarturl') ) {
										var webform = document.getElementById('webform1011088000000647216');
										var service = urlparams.get('service');
										var smarturlfield = document.createElement('input');
										smarturlfield.setAttribute('type', 'hidden');
										smarturlfield.setAttribute('value', service);
										smarturlfield.setAttribute('name', 'service');
										webform.appendChild(smarturlfield);
									}
									document.querySelector('.crmWebToEntityForm .formsubmit').setAttribute('disabled', true);
								}
								function tooltipShow1011088000000647216(el){
									var tooltip = el.nextElementSibling;
									var tooltipDisplay = tooltip.style.display;
									if (tooltipDisplay == 'none') {
										var allTooltip = document.getElementsByClassName('zcwf_tooltip_over');
										for (i = 0; i < allTooltip.length; i++ ) {
											allTooltip[i].style.display = 'none';
										}
										tooltip.style.display = 'block';
									} else {
										tooltip.style.display = 'none';
									}
								}
