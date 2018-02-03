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
			'target_name': 'lcs-check',
			'type': 'none',

			'dependencies':
			[
				'../toolchain/lc-compile/lc-compile.gyp:lc-compile',
				'../engine/engine.gyp:standalone',
				'../revzip/revzip.gyp:external-revzip',
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
