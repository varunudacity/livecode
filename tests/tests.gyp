{
	'includes':
	[
		'../common.gypi',
	],

    'variables':
    {
        'conditions':
        [
            [
                'host_os == "linux"',
                {
                    'server-engine': '<(PRODUCT_DIR)/server-community',
                    'dev-engine': '<(PRODUCT_DIR)/LiveCode-Community',
                    'standalone-engine': '<(PRODUCT_DIR)/standalone-community',                                        
                },
            ],
            [
                'host_os == "mac"',
                {
                    'server-engine': '<(PRODUCT_DIR)/server-community',
                    'dev-engine': '<(PRODUCT_DIR)/LiveCode-Community.app/Contents/MacOS/LiveCode-Community',
                    'standalone-engine': '<(PRODUCT_DIR)/Standalone-Community.app/Contents/MacOS/Standalone-Community',   
                },
            ],
            [
                'host_os == "win"',
                {
                    'server-engine': '<(PRODUCT_DIR)/server-community.exe',
                    'dev-engine': '<(PRODUCT_DIR)/LiveCode-Community.exe',
                    'standalone-engine': '<(PRODUCT_DIR)/standalone-community.exe',   
                },
            ],
        ],
    },
    
    'targets':
    [
		{
			'target_name': 'tests-run-all',
			'type': 'none',

			'dependencies':
			[
				'lcs-check',				
			],

		},
		{
			'target_name': 'lcs-check-modules',
			'type': 'none',
			
			'dependencies':
			[
				'../toolchain/lc-compile/lc-compile.gyp:lc-compile',
				'../engine/lcb-modules.gyp:engine_lcb_modules',
				'../engine/engine.gyp:server',			
			],

			'actions':
			[
				{
					'action_name': 'compile_modules',

					'inputs':
					[
						'test-extensions-utils.lc',
					],

					'outputs':
					[
						# hack because gyp wants an output
                        'notarealfile.txt',
					],

					'message': 'Compiling modules for lcs tests',

					'action':
					[
						'<(server-engine)',
						'test-extensions-utils.lc',
						'$(not_a_real_variable)findandcompile',
						'lcs'
					],
				},
			],			
		},		
		{
			'target_name': 'lcs-check-extensions-compile',
			'type': 'none',
			
			'dependencies':
			[
				'../toolchain/lc-compile/lc-compile.gyp:lc-compile',
				'../engine/lcb-modules.gyp:engine_lcb_modules',
				'../engine/engine.gyp:server',
				'../revzip/revzip.gyp:external-revzip-server',				
			],

			'actions':
			[
				{
					'action_name': 'build_extensions',

					'inputs':
					[
						'test-extensions-utils.lc',
					],

					'outputs':
					[
						# hack because gyp wants an output
                        'notarealfile.txt',
					],

					'message': 'Building extensions for lcs tests',

					'action':
					[
						'<(server-engine)',
						'test-extensions-utils.lc',
						'$(not_a_real_variable)findandbuild',
						'lcs/extensions',
						'../ide-support/revdocsparser.livecodescript',
						'../_tests/_build/packaged_extensions',
						'$(not_a_real_variable)false',
						'>(lc-compile_host)',
						'<(PRODUCT_DIR)/modules/lci',
					],
				},
			],			
		},
		{
			'target_name': 'lcs-check',
			'type': 'none',

			'dependencies':
			[
				'../engine/engine.gyp:standalone',
				'../revzip/revzip.gyp:external-revzip',
				'../revdb/revdb.gyp:external-revdb',
				'../revdb/revdb.gyp:dbsqlite',
				'../thirdparty/libopenssl/libopenssl.gyp:revsecurity',
				'../extensions/extensions.gyp:extensions',
				'lcs-check-extensions-compile',
				'lcs-check-modules',
			],
					
			'actions':
			[
				{
					'action_name': 'lcs_check',

					'inputs':
					[
						'_testrunner.livecodescript',
					],

					'outputs':
					[
						# hack because gyp wants an output
                        'notarealfile.txt',
					],

					'message': 'Testing standalone engine',

					'action':
					[
						'<(standalone-engine)',
						'<@(_inputs)',
						'run',
						'lcs',
					],
				},
			],
		},
	],
}
